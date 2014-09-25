#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import random
from action import base_manager
from bottle import redirect
from entity import user as user_entity
from helper import hint
from helper import translator
from helper import url


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

    def action(self, language, pw_hash_iterations, admin_user):
        """ Handle actions. Returns hints or redirects. """
        _ = translator.Translator.instance(language)

        if self.get_form('action') == 'login':
            user_name = self.get_form('name')
            password = self.get_form('password')
            if not user_name or not password:
                hint_text = _('Please provide your user name and password.')
                self.hints.append(hint.Hint(hint_text))
                return self.hints

            user = user_entity.User.find_name(self.db, user_name)
            hint_text = _('Given user name or password is wrong. Please '
                          'try again.')
            redirect_url = url.Url.from_path([''])
            if not user:
                user_count = user_entity.User.count_all(self.db)
                if not user_count and user_name == admin_user:
                    admin_hash = self.__admin_hash(admin_user,
                                                   pw_hash_iterations)
                    self.set_cookie(self.SESSION_COOKIE, admin_hash)
                    redirect(redirect_url)
                else:
                    self.hints.append(hint.Hint(hint_text))
                    return self.hints

            pw_hash = self.__generate_pw_hash(password, user.salt,
                                              pw_hash_iterations)
            if pw_hash != user.pw_hash:
                self.hints.append(hint.Hint(hint_text))
                return self.hints
            else:
                session_number = str(random.randint(0, 10000000000000000000000))
                session = self.__generate_pw_hash(session_number, user.salt,
                                                  pw_hash_iterations)
                self.set_cookie(self.USER_NAME_COOKIE, user.name)
                self.set_cookie(self.SESSION_COOKIE, session)
                user.session = session
                user.save(self.db)
                redirect(redirect_url)

        return self.hints

    def current_user(self):
        """ Returns the current user or None. """
        if not self._current_user:
            user_name = self.get_cookie(self.USER_NAME_COOKIE)
            if user_name:
                self._current_user = user_entity.User.find_name(self.db, user_name)
        return self._current_user

    def validate_login(self, pw_hash_iterations, admin_user):
        """ Validates if a user is logged in. """
        session = self.get_cookie(self.SESSION_COOKIE)
        user = self.current_user()
        if not user or not user.session or user.session != session:
            user_count = user_entity.User.count_all(self.db)
            admin_hash = self.__admin_hash(admin_user, pw_hash_iterations)
            if user_count or (session != admin_hash):
                redirect(url.Url.from_path(['login']))

    def __admin_hash(self, admin_user, iterations):
        """ Calculate admin hash for first login. """
        return self.__generate_pw_hash(admin_user, admin_user,
                                       iterations)

    def __generate_pw_hash(self, password, salt, iterations):
        """ Returns the password hash. """
        pw_hash = hashlib.sha512(bytes(password + salt, 'utf-8')).hexdigest()
        for x in range(0, iterations):
            pw_hash = hashlib.sha512(bytes(pw_hash, 'utf-8')).hexdigest()
        return pw_hash