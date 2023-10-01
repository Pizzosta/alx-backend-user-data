#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash the input password using bcrypt with a generated salt.

    Args:
        password (str): The input password.

    Returns:
        bytes: The salted hash of the input password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password
