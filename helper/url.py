#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import unicodedata
import urllib


class Url:
    """ Generates URLs. """

    @staticmethod
    def from_category(category, absolute=None):
        """ Generates a URL from a category. Returns relative URL string. If
        absolute is set to the domain the returned URL will be absolute. """
        path_parts = ['category',
                      '{}-{}'.format(category.id, category.name.lower())]
        return Url.from_path(path_parts, absolute, True)

    @staticmethod
    def from_css(css_file, absolute=None):
        """ Generates a URL from a css file name. Returns relative URL string.
        If absolute is set to the domain the returned URL will be absolute. """
        return Url.from_path(['css', css_file], absolute)

    @staticmethod
    def from_img(img_file, absolute=None):
        """ Generates a URL from a image file name. Returns relative URL string.
        If absolute is set to the domain the returned URL will be absolute. """
        url = urllib.parse.quote(img_file)
        if absolute:
            url = absolute + url
        return url

    @staticmethod
    def from_js(js_file, absolute=None):
        """ Generates a URL from a css file name. Returns relative URL string.
        If absolute is set to the domain the returned URL will be absolute. """
        return Url.from_path(['js', js_file], absolute)

    @staticmethod
    def from_path(path_parts, absolute=None, filter_chars=False):
        """ Generates a URL from a list of path parts. Returns relative
        URL string. If absolute is set to the domain the returned URL will
        be absolute. If filter_chars is true special characters are replaced. """
        if filter_chars:
            path_parts = [Url.slugify(part) for part in path_parts]
        url = '/'.join(path_parts)
        url = '/' + url

        if absolute:
            url = absolute + url
        return url

    @staticmethod
    def from_recipe(recipe, absolute=None):
        """ Generates a URL from a recipe. Returns relative URL string. If
        absolute is set to the domain the returned URL will be absolute. """
        path_parts = ['recipe',
                      '{}-{}'.format(recipe.id, recipe.title.lower())]
        return Url.from_path(path_parts, absolute, True)

    @staticmethod
    def search(search_text, absolute=None):
        """ Generates a URL for search. Returns relative URL string. If
        absolute is set to the domain the returned URL will be absolute. """
        url = '/search?q={}'.format(urllib.parse.quote(search_text))
        if absolute:
            url = absolute + url
        return url

    @staticmethod
    def slugify(text):
        """ Normalizes string, converts to lowercase, removes non-alpha
        characters and converts spaces to hyphens.
        See http://stackoverflow.com/a/7871982/1931663
        """
        text = text.replace('ß', 'ss')
        text = unicodedata.normalize('NFKD', text).\
            encode('ascii', 'ignore').\
            decode('ascii')
        text = re.sub('[^\w\s-]', '', text).strip().lower()
        return re.sub('[-\s]+', '-', text)