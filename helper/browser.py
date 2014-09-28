#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from bottle import request

class Browser:
    """ Gives access to browser specific information.

    Constants:
    RE_BOT -- Regular expression to identify bots (string)
    RE_DESKTOP -- Regular expression to identify desktop browsers (string)
    RE_MOBILE -- Regular expression to identify bots. See https://developer.mozilla.org/en-US/docs/Browser_detection_using_the_user_agent#Mobile.2C_Tablet_or_Desktop (string)
    """

    RE_BOT = re.compile(r'(spider|crawl|slurp|bot)', re.I)
    RE_DESKTOP = re.compile(r'(windows|linux|os\s+[x9]|solaris|bsd)', re.I)
    RE_MOBILE = re.compile(r'(Mobi)', re.I)

    @classmethod
    def is_bot(cls):
        """ Checks if a user agent corresponds to a bot. """
        return bool(cls.RE_BOT.search(cls.user_agent()))

    @classmethod
    def is_desktop(cls):
        """ Checks if a user agent corresponds to a desktop browser. """
        is_desktop = bool(cls.RE_DESKTOP.search(cls.user_agent()))
        return not cls.is_mobile() and (is_desktop or cls.is_bot())

    @classmethod
    def is_mobile(cls):
        """ Checks if a user agent corresponds to a mobile browser. """
        return bool(cls.RE_MOBILE.search(cls.user_agent()))

    @staticmethod
    def user_agent():
        """ Returns the user agent. """
        return request.get_header('User-Agent', '')