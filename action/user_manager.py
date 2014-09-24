#!/usr/bin/python
# -*- coding: utf-8 -*-

from action import base_manager
from bottle import redirect
from entity import user as user_entity


class UserManager(base_manager.BaseManager):
    """ Handle user related actions.

    Constants:
    SESSION_COOKIE -- The session cookie (string).
    USER_NAME_COOKIE -- The user name cookie (string).

    Member:
    db -- The database connection.
    hints -- List of hints which occurred during action handling (list hint).
    _current_user -- Cache for current user (user).
    """

    SESSION_COOKIE = 'session'
    USER_NAME_COOKIE = 'user'

    def __init__(self, db):
        self.db = db
        self.hints = []
        self._current_user = None

    def current_user(self):
        """ Returns the current user or None. """
        if not self._current_user:
            user_name = self.get_cookie(self.USER_NAME_COOKIE)
            if user_name:
                self._current_user = user_entity.User.find_name(self.db, user_name)
        return self._current_user

    def validate_login(self):
        """ Validates if a user is logged in. """
        session = self.get_cookie(self.SESSION_COOKIE)
        user = self.current_user()
        if not user or not user.session or user.session != session:
            redirect('/login')