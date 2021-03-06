#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import request
from bottle import response

class BaseManager:
    """ Base class for manager.

    Constants:
    COOKIE_PATH -- Global cookie path (string).
    """

    COOKIE_PATH = '/'

    def delete_cookie(self, name):
        """ Delete cookie. """
        response.delete_cookie(name, path=self.COOKIE_PATH)

    def get_cookie(self, name):
        """ Returns cookie value. """
        return request.get_cookie(name)

    def get_form(self, name, strip_value=True):
        """ Returns form value for name. """
        request.forms.recode_unicode = False
        value = request.forms.getunicode(name)
        if strip_value and value:
            value = value.strip()
        return value

    def set_cookie(self, name, value, httponly=True, expires=None):
        """ Set cookie. """
        if not expires:
            response.set_cookie(name, value, httponly=httponly,
                                path=self.COOKIE_PATH)
        else:
            response.set_cookie(name, value, httponly=httponly,
                                path=self.COOKIE_PATH, expires=expires)