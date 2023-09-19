#!/usr/bin/env python3

""" Handles all routes for the Session Expiry authentication
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Expiry Class"""

    def __init__(self):
        """Initialize a SessionExpAuth instance"""
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Creates a new Session ID for a User"""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get the user ID associated with a session ID"""
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)

        if not session_data:
            return None

        if self.session_duration <= 0:
            return session_data.get('user_id')

        created_at = session_data.get('created_at')

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_data.get('user_id')
