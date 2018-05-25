#!/bin/bash

# Print script trace
set -x

# Abort on failure
set -e

# Enable colored output
export ANSIBLE_FORCE_COLOR=true

# Export manual AWS profile selection
export ANSIBLE_AWS_PROFILE

# Print Ansible version
ansible --version

# Dump the current environment
env | grep -v TERMCAP | sort

# vim: set ts=2 sts=2 sw=2 et:
