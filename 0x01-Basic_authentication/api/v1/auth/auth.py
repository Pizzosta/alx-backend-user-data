#!/usr/bin/env python3
"""Authentication Module"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Auth Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path."""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for excluded_path in excluded_paths:
                if path.endswith('/') and path == excluded_path[:-1]:
                    return False
                if not path.endswith('/') and path + '/' == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the authorization header from the request."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request."""
        return None
