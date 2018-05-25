# Checklist for new Ansible project

- Set region in `group_vars/all/aws.yml`, `inventory/ec2.ini` and `vars_plugins/aws.yml`
- Replace all occurrences of `acme` with customer shortname
- Replace all occurrences of `acme.net` with customer domain(s)
- Follow all `TODO` markers
- Set subnet groups in `vars_plugins/aws.yml`
- Generate vault password
- Generate ssh keys for Ansible and CI
- Set up CI user on GitHub/Bitbucket and add ssh pubkey
- Launch sysadmin instance
- Transfer to sysadmin instance and set `vpc_destination_variable = private_ip_address` in `inventory/ec2.ini`
- Launch jenkins and ansible instances
- Remove this file
