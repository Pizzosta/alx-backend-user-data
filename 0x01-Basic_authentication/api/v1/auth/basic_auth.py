#!/usr/bin/env python3
""" Definition of class BasicAuth Module """
from .auth import Auth


class BasicAuth(Auth):
    """ Implement Basic Authorization protocol methods """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        base64_part = authorization_header.split(" ")[1]
        return base64_part
