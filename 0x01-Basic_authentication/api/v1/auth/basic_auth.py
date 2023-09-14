#!/usr/bin/env python3
""" Definition of class BasicAuth Module """
import base64
from typing import TypeVar
from models.user import User
from .auth import Auth


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
        base64_part = authorization_header.split(" ")[-1]
        return base64_part

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of a Base64 string
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ returns the user email and password
        from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        split_result = decoded_base64_authorization_header.split(':', 1)
        if len(split_result) != 2:
            return None, None
        user_email, user_password = split_result

        return user_email, user_password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user_instances = User.search({"email": user_email})
            if user_instances is None:
                return None

            for user_instance in user_instances:
                if User.is_valid_password(user_instance, user_pwd):
                    return user_instance

            return None
        except Exception:
            None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user from the request. """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_part = self.extract_base64_authorization_header(auth_header)
        if base64_part is None:
            return None

        decoded_value = self.decode_base64_authorization_header(base64_part)
        if decoded_value is None:
            return None

        user_email, user_password = self.extract_user_credentials(
            decoded_value)
        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
