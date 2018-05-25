#!/bin/bash

DIR=$(cd `dirname $0` && pwd)

[[ -z "${ANSIBLE_CONFIG}" ]] && export ANSIBLE_CONFIG="${DIR}/ansible.cfg"
[[ -z "${ANSIBLE_VAULT_PASSWORD_FILE}" ]] && export ANSIBLE_VAULT_PASSWORD_FILE="${HOME}/secrets/acme-vault-password.txt"

ansible-vault "$@"
exit $?

# vim: set ts=2 sts=2 sw=2 et:
