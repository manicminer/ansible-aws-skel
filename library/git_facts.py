#!/usr/bin/python

DOCUMENTATION = '''
---
module: git_facts
version_added: "devel"
short_description: retrieve facts about a git repository
description:
     - retrieve facts about a git repository. This module has a dependency on GitPython.
options:
  name:
    description:
      - Arbitrary name for repository. Facts will be registered using this name.
    required: true
    default: null
    aliases: []
  repo:
    description:
      - Path to repository where facts should be gathered.
    required: true
    default: null
    aliases: []
requirements: [ "git" ]
author: Tom Bamford
'''

EXAMPLES = '''
# Get some facts about a repository
- git_facts:
    name: myproject
    repo: /path/to/myproject

# Access gathered facts
- debug:
    var: git_facts.myproject
'''

import sys
import time
import json

try:
    from git import *
except ImportError:
    print "failed=True msg='GitPython required for this module'"
    sys.exit(1)


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name = dict(required=True, default=None),
            repo = dict(required=True, default=None),
        ),
    )
    params = module.params
    name = params['name']
    repo_path = params['repo']

    repo = Repo(repo_path)

    repo_info = dict()
    if not repo.head.is_detached:
        repo_info['branch'] = repo.active_branch.name
    repo_info['repo_dirty'] = repo.is_dirty()
    repo_info['untracked_files'] = repo.untracked_files
    headcommit = repo.head.commit
    repo_info['date'] = time.strftime("%Y-%m-%d", time.gmtime(headcommit.committed_date))
    repo_info['message'] = headcommit.message
    repo_info['sha'] = headcommit.hexsha[0:7]
    repo_info['sha_full'] = headcommit.hexsha
    repo_info['time'] = time.strftime("%H:%M:%S", time.gmtime(headcommit.committed_date))
    repo_info['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(headcommit.committed_date))

    fact_name = "git_facts_%s" % name

    sys.stdout.write(json.dumps({
        'changed': False,
        'ansible_facts': {
            fact_name: repo_info,
        },
    }))


from ansible.module_utils.basic import *
main()

# vim: set ts=4 sts=4 sw=4 expandtab:
