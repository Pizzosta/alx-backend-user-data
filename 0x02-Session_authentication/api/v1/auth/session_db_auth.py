#!/usr/bin/env python3
"""Definition of class SessionDBAuth Module """

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    def create_session(self, user_id=None):
        """Create and store a new UserSession instance
        and return the Session ID.
        """
        session_id = super().create_session(user_id)

        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get the user ID associated with a session ID
        by querying UserSession in the database.
        """
        if session_id is None:
            return None

        user_session = UserSession.search({"session_id": session_id})

        if not user_session or user_session == []:
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the Session ID
        from the request cookie.
        """
        session_id = self.session_cookie(request)

        if session_id:
            user_sessions = UserSession.search({"session_id": session_id})

            if user_sessions and user_sessions != []:
                for user_session in user_sessions:
                    user_session.remove()
                    return True

        return False
