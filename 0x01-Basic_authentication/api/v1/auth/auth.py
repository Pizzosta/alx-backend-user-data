#!/usr/bin/env python3
"""Authentication Module"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Auth Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path."""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and \
                    path.startswith(excluded_path[:-1]):
                return False
            elif excluded_path in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the authorization header from the request."""
        if request is None:
            return None
        elif 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request."""
        return None
