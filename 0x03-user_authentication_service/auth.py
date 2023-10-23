#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


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


def _generate_uuid() -> str:
    """Generate a new UUID and return it as a string."""
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and password.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            self._db.find_user_by(email=email)

        except NoResultFound:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid for login.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Create a session for the user and return the session ID."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Takes a session_id and returns the corresponding user, if one exists,
        else returns None
        Args:
            session_id (str): session id for user
        Return:
            user object if found, else None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Take a user_id and destroy that user's session and update their
        session_id attribute to None
        Args:
            user_id (int): user's id
        Return:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None
