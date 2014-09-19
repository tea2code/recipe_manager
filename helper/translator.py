#!/usr/bin/python
# -*- coding: utf-8 -*-

import gettext
from bottle import request

class TranslatorNotInitializedError(Exception):
    """ Exception raised if Translator is not initialized. """


class Translator:
    """ Wrapper for gettext for translations.

    Member:
    translations -- Dict of gettext translation instances.
    """

    translations = {}

    @staticmethod
    def current_language(default_language):
        """ Returns the current language. """
        return request.get_cookie('language', default_language)

    @staticmethod
    def init(language, path):
        """ Initialize translator. Must be called before first call to
        instance. """
        if language in Translator.translations:
            return
        Translator.language = language
        Translator.translations[language] = gettext.translation(
            language,
            localedir=path,
            languages=[language],
            fallback=True)

    @staticmethod
    def instance(language):
        """ Returns a translator instance for given language. """
        if language not in Translator.translations:
            msg = 'Language {} not initialized'.format(language)
            raise TranslatorNotInitializedError(msg)
        return Translator.translations[language].gettext