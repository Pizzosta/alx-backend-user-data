#!/usr/bin/env python3
"""Module Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with salt

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        bytes: A salted, hashed password as a byte string
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password using bcrypt.

    Args:
        hashed_password (bytes): The hashed password as a byte string.
        password (str): The plain text password to be validated.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)
