#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import html_escape

class HtmlEscape:
    """ Wrapper for custom escape functions. """

    @staticmethod
    def html_escape_nl2br(text):
        """ Escapes text and replaces \n with <br>. """
        return html_escape(text).replace('\n', '<br>')