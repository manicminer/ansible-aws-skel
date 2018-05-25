#!/usr/bin/env python
from passlib.hash import sha512_crypt
import sys

if len(sys.argv) == 2:
    print(sha512_crypt.encrypt(sys.argv[1]))
else:
    print("usage: {0} PASSWORD\n".format(sys.argv[0]))

# vim: set ft=python ts=4 sts=4 sw=4 et:
