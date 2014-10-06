#!/usr/bin/python
# -*- coding: utf-8 -*-


class JsonLink:
    """ Object representing a link.

    Member:
    name -- The optional link name (string).
    url -- The link url (string).
    """

    def __init__(self, name='', url=''):
        self.name = name
        self.url = url


class JsonRecipe:
    """ Simplified recipe object for json import and export.

    Member:
    description -- The cooking description (string).
    images -- List of image names (list string).
    info -- Additional information (string).
    ingredients -- The ingredients (string).
    serving_size -- A short description of the serving size (string).
    synonyms -- List of synonyms for the title (list string).
    title -- The title (string).
    urls -- List of urls (list jsonlink).
    """

    def __init__(self, description='', info='', ingredients='', serving_size='',
                 title='', urls=[], synonyms=[], images=[]):
        self.description = description
        self.id = id
        self.images = images
        self.info = info
        self.ingredients = ingredients
        self.serving_size = serving_size
        self.synonyms = synonyms
        self.title = title
        self.urls = urls