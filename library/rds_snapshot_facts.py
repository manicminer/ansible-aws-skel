#!/usr/bin/python
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: rds_snapshot_facts
short_description: searches for rds snapshots to obtain the id
description:
    - searches for rds snapshots to obtain the id
options:
  snapshot_id:
    description:
      - id of the snapshot to search for
    required: false
  instance_id:
    description:
      - id of a DB instance
    required: false
  max_records:
    description:
      - max records returned
    required: false
  id_regex:
    description:
      - Filter the results by matching this regular expression against the snapshot ID.
    default: null
    required: false
  snapshot_type:
    description:
      - Filter the results by snapshot type.
    choices: ['automated', 'manual']
    default: null
    required: false
  sort:
    description:
      - Optional attribute which with to sort the results.
    choices: ['id', 'snapshot_create_time']
    default: null
    required: false
  sort_order:
    description:
      - Order in which to sort results.
      - Only used when the 'sort' parameter is specified.
    choices: ['ascending', 'descending']
    default: 'ascending'
    required: false
  sort_start:
    description:
      - Which result to start with (when sorting).
      - Corresponds to Python slice notation.
    default: null
    required: false
  sort_end:
    description:
      - Which result to end with (when sorting).
      - Corresponds to Python slice notation.
    default: null
    required: false
  status:
    description:
      - Filter the results by snapshot status.
    choices:
      - available
      - backing-up
      - creating
      - deleted
      - deleting
      - failed
      - modifying
      - rebooting
      - resetting-master-credentials
    default: null
    required: false

author: "Brock Haywood (@brockhaywood), Tom Bamford (@tombamford)"
extends_documentation_fragment:
    - aws
    - ec2
'''

EXAMPLES = '''
# Basic Snapshot Search
- local_action:
    module: rds_snapshot_facts
    snapshot_id: my-local-snapshot

# Find all
- local_action:
    module: rds_snapshot_facts

# Find latest, available, automated snapshot
- local_action:
    module: rds_snapshot_facts
    instance_id: my-rds-instance
    snapshot_type: automated
    sort: snapshot_create_time
    sort_order: descending
    sort_end: 1
    status: available
'''

try:
    import boto.rds
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


def find_snapshot_facts(module, conn, snapshot_id=None, instance_id=None, max_records=None, id_regex=None, snapshot_type=None, sort=None, sort_order=None, sort_start=None, sort_end=None, status=None):

    try:
        snapshots = conn.get_all_dbsnapshots(snapshot_id=snapshot_id, instance_id=instance_id, max_records=max_records)
    except boto.exception.BotoServerError, e:
        module.fail_json(msg="%s: %s" % (e.error_code, e.error_message))

    results = []

    for snapshot in snapshots:
    
        data = {
            'engine_version': snapshot.engine_version,
            'allocated_storage': snapshot.allocated_storage,
            'availability_zone': snapshot.availability_zone,
            'id': snapshot.id,
            'instance_create_time': snapshot.instance_create_time,
            'instance_id': snapshot.instance_id,
            'master_username': snapshot.master_username,
            'iops': snapshot.iops,
            'port': snapshot.port,
            'status': snapshot.status,
            'option_group_name': snapshot.option_group_name,
            'snapshot_create_time': snapshot.snapshot_create_time,
            'snapshot_type': snapshot.snapshot_type,
            'source_region': snapshot.source_region,
            'vpc_id': snapshot.vpc_id
        }

        if id_regex:
            regex = re.compile(id_regex)
            if not regex.match(data['id']):
                continue

        if snapshot_type:
            if data['snapshot_type'] != snapshot_type:
                continue

        if status:
            if data['status'] != status:
                continue

        results.append(data)

    if sort:
        results.sort(key=lambda e: e[sort], reverse=(sort_order=='descending'))

    try:
        if sort and sort_start and sort_end:
            results = results[int(sort_start):int(sort_end)]
        elif sort and sort_start:
            results = results[int(sort_start):]
        elif sort and sort_end:
            results = results[:int(sort_end)]
    except TypeError:
        module.fail_json(msg="Please supply numeric values for sort_start and/or sort_end")

    module.exit_json(results=results)


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            snapshot_id=dict(),
            instance_id=dict(),
            max_records=dict(),
            id_regex=dict(required=False, default=None),
            snapshot_type=dict(required=False, default=None,
                choices=['automated', 'manual']),
            sort = dict(required=False, default=None,
                choices=['id', 'snapshot_create_time']),
            sort_order = dict(required=False, default='ascending',
                choices=['ascending', 'descending']),
            sort_start = dict(required=False),
            sort_end = dict(required=False),
            status = dict(required=False, default=None,
                choices=['available', 'backing-up', 'creating', 'deleted',
                         'deleting', 'failed', 'modifying', 'rebooting',
                         'resetting-master-credentials']),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO:
        module.fail_json(msg='boto required for this module')

    snapshot_id = module.params.get('snapshot_id')
    instance_id = module.params.get('instance_id')
    max_records = module.params.get('max_records')
    id_regex = module.params.get('id_regex')
    snapshot_type = module.params.get('snapshot_type')
    sort = module.params.get('sort')
    sort_order = module.params.get('sort_order')
    sort_start = module.params.get('sort_start')
    sort_end = module.params.get('sort_end')
    status = module.params.get('status')

    # Retrieve any AWS settings from the environment.
    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module)

    if not region:
        module.fail_json(msg=str("Either region or AWS_REGION or EC2_REGION "
                                 "environment variable or boto config "
                                 "aws_region or ec2_region must be set."))

    try:
        conn = connect_to_aws(boto.rds, region, **aws_connect_kwargs)

        find_snapshot_facts(
            module=module,
            conn=conn,
            snapshot_id=snapshot_id,
            instance_id=instance_id,
            max_records=max_records,
            id_regex=id_regex,
            snapshot_type=snapshot_type,
            sort=sort,
            sort_order=sort_order,
            sort_start=sort_start,
            sort_end=sort_end,
            status=status
        )

    except boto.exception.BotoServerError, e:
        module.fail_json(msg=e.error_message)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

if __name__ == '__main__':
    main()
