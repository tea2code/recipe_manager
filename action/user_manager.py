#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import random
import uuid
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
        """ Handle actions. Returns users or redirects. """
        # Validate user and initialize admin user if necessary.
        self.validate_login(pw_hash_iterations, admin_user)
        is_admin = (self.current_user().name == admin_user)
        if is_admin:
            users = self.__action_admin(language, pw_hash_iterations)
        else:
            users = self.__action_user(language, pw_hash_iterations)
        return users

    def current_user(self):
        """ Returns the current user or None. """
        if not self._current_user:
            user_name = self.get_cookie(self.USER_NAME_COOKIE)
            if user_name:
                self._current_user = user_entity.User.find_name(self.db, user_name)
        return self._current_user

    def login(self, language, pw_hash_iterations, admin_user):
        """ Handle login. Returns hints or redirects. """
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
                session_salt = self.__generate_salt()
                session = self.__generate_pw_hash(session_salt, user.salt,
                                                  pw_hash_iterations)
                expires = datetime.datetime.now() + datetime.timedelta(days=365)
                self.set_cookie(self.USER_NAME_COOKIE, user.name, expires=expires)
                self.set_cookie(self.SESSION_COOKIE, session, expires=expires)
                user.session = session
                user.save(self.db)
                redirect(redirect_url)

        return self.hints

    def logout(self):
        """ Log user out. """
        user = self.current_user()
        if user and user.id:
            user.session = None
            user.save(self.db)
        self.delete_cookie(self.USER_NAME_COOKIE)
        self.delete_cookie(self.SESSION_COOKIE)
        redirect(url.Url.from_path(['']))

    def validate_login(self, pw_hash_iterations, admin_user):
        """ Validates if a user is logged in. """
        session = self.get_cookie(self.SESSION_COOKIE)
        user = self.current_user()
        if not user or not user.session or user.session != session:
            user_count = user_entity.User.count_all(self.db)
            admin_hash = self.__admin_hash(admin_user, pw_hash_iterations)
            is_admin = (session == admin_hash)
            if is_admin:
                # Create fake user. Dangerous! Always check "user and user.id".
                self._current_user = user_entity.User(name=admin_user)
            if user_count or not is_admin:
                redirect(url.Url.from_path(['login']))

    def __action_admin(self, language, pw_hash_iterations):
        """ Handle admin actions. Returns users or redirects. """
        _ = translator.Translator.instance(language)

        action = self.get_form('action')
        if action == 'new':
            user_name = self.get_form('name')
            password = self.get_form('password')
            password_confirm = self.get_form('password-confirm')
            if not user_name or not password:
                hint_text = _('Please provide user name and password.')
                self.hints.append(hint.Hint(hint_text))
            elif password != password_confirm:
                hint_text = _('Both passwords are not the same.')
                self.hints.append(hint.Hint(hint_text))
            elif user_entity.User.find_name(self.db, user_name):
                hint_text = _('User name is already taken.')
                self.hints.append(hint.Hint(hint_text))
            else:
                user = user_entity.User(name=user_name)
                user.salt = self.__generate_salt()
                user.pw_hash = self.__generate_pw_hash(password, user.salt,
                                                  pw_hash_iterations)
                user.save(self.db)
                hint_text = _('User "{}" has been created.').format(user_name)
                self.hints.append(hint.Hint(hint_text))

        elif action == 'edit':
            id = self.get_form('id')
            user = user_entity.User.find_pk(self.db, id)
            is_delete = self.get_form('delete') is not None
            if is_delete:
                hint_text = _('User "{}" has been deleted.').format(user.name)
                user.delete(self.db)
                self.hints.append(hint.Hint(hint_text))
            else:
                password = self.get_form('password')
                password_confirm = self.get_form('password-confirm')
                if not password:
                    hint_text = _('Please provide the password.')
                    self.hints.append(hint.Hint(hint_text))
                elif password != password_confirm:
                    hint_text = _('Both passwords are not the same.')
                    self.hints.append(hint.Hint(hint_text))
                else:
                    user.salt = self.__generate_salt()
                    user.pw_hash = self.__generate_pw_hash(password, user.salt,
                                                           pw_hash_iterations)
                    user.session = None
                    user.save(self.db)
                    hint_text = _('User "{}" has been updated.').format(user.name)
                    self.hints.append(hint.Hint(hint_text))

        return user_entity.User.find_all(self.db)

    def __action_user(self, language, pw_hash_iterations):
        """ Handle user actions. Returns users or redirects. """
        _ = translator.Translator.instance(language)

        action = self.get_form('action')
        if action == 'edit-profile':
            password = self.get_form('password')
            password_confirm = self.get_form('password-confirm')
            if not password:
                hint_text = _('Please provide the password.')
                self.hints.append(hint.Hint(hint_text))
            elif password != password_confirm:
                hint_text = _('Both passwords are not the same.')
                self.hints.append(hint.Hint(hint_text))
            else:
                user = self.current_user()
                user.salt = self.__generate_salt()
                user.pw_hash = self.__generate_pw_hash(password, user.salt,
                                                       pw_hash_iterations)
                user.session = None
                user.save(self.db)
                hint_text = _('Your profile has been updated. Please login '
                              'again.')
                self.hints.append(hint.Hint(hint_text))
        return []

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

    def __generate_salt(self):
        """ Generates a random salt. """
        return uuid.uuid4().hex