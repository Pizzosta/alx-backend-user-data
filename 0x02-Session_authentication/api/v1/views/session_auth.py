#!/usr/bin/env python3

""" Handles all routes for the Session authentication
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    from api.v1.app import auth

    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user_instances = User.search({"email": email})

    if not user_instances:
        return jsonify({"error": "no user found for this email"}), 404

    for user_instance in user_instances:
        if not User.is_valid_password(user_instance, password):
            return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user_instance.id)
    session_name = getenv('SESSION_NAME')

    response = jsonify(user_instance.to_json())
    response.set_cookie(session_name, session_id)

    return response
