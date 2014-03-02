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

    def get_form(self, name):
        """ Returns form value for name. """
        request.forms.recode_unicode = False
        return request.forms.getunicode(name)

    def set_cookie(self, name, value, httponly=True):
        """ Set cookie. """
        response.set_cookie(name, value, httponly=httponly,
                            path=self.COOKIE_PATH)