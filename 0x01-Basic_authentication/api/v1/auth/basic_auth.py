#!/usr/bin/env python3
""" Definition of class BasicAuth Module """
from .auth import Auth
import base64


class BasicAuth(Auth):
    """ Implement Basic Authorization protocol methods """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        base64_part = authorization_header.split(" ")[1]
        return base64_part

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """that returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_value.decode("utf-8")
            return decoded_str
        except Exception:
            None
