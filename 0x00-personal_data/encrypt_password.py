#!/usr/bin/env python3
"""Module Encrypting passwords"""

import bcrypt

def hash_password(password: str)-> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return hashed_password