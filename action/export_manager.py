#!/usr/bin/python
# -*- coding: utf-8 -*-

import bottle
import io
import json
import zipfile
from action import base_manager
from entity import recipe as recipe_entity
from helper import url as url_helper


class ExportManager(base_manager.BaseManager):
    """ Handles export actions.

    Member:
    db -- The database connection.
    """

    def __init__(self, db):
        self.db = db

    def action(self, static_path, image_path, id, recipe_json):
        """ Exports recipe with given id. Returns download stream. """

        recipe = recipe_entity.Recipe.find_pk(self.db, id)

        # Convert recipe to json compatible object.
        images = [image.path.replace(image_path, '')
                  for image in recipe.images]
        urls = [{'name': url.name, 'url': url.url} for url in recipe.urls]
        synonyms = [synonym.name for synonym in recipe.synonyms]
        json_obj = {
            'description': recipe.description,
            'info': recipe.info,
            'ingredients': recipe.ingredients,
            'serving_size': recipe.serving_size,
            'title': recipe.title,
            'urls': urls,
            'synonyms': synonyms,
            'images': images
        }

        # Create json.
        json_str = json.dumps(json_obj)

        # Create zip.
        with io.BytesIO() as zip_bytes:
            with zipfile.ZipFile(zip_bytes, mode='w') as zip:
                zip.writestr(recipe_json, json_str)
                for image in recipe.images:
                    index = image.path.rfind('/')
                    file_name = image.path[index:]
                    zip.write(static_path+'/'+image.path, file_name)
            result = zip_bytes.getvalue()

        # Stream to browser.
        name = url_helper.Url.slugify(recipe.title)
        bottle.response.set_header('Content-Disposition',
                                   'attachment; filename={}.zip'.format(name))
        bottle.response.set_header('Content-Type', 'application/zip')
        return result