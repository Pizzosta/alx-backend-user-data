#!/usr/bin/env python3
""" Definition of class SessionAuth Module """
from uuid import uuid4
from .auth import Auth


class SessionAuth(Auth):
    """Implement Session Authorization protocol methods"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id and store it."""
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a User ID based on a Session ID"""
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
