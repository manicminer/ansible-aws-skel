#!/bin/bash

DIR=$(cd `dirname $0` && pwd)

find . -type f -name '*.yml' -print0 | xargs -0 grep -l '^\$ANSIBLE_VAULT;' | while read f; do
  "${DIR}"/vault.sh view "$f" | grep -i $@ | while read r; do
    echo "$f: $r"
  done
done

# vim: set ts=2 sts=2 sw=2 et:
