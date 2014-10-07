#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from action import base_manager
from action import user_manager
from bottle import redirect
from bottle import request
from entity import category as category_entity
from entity import image as image_entity
from entity import recipe as recipe_entity
from entity import synonym as synonym_entity
from entity import tag as tag_entity
from entity import url as url_entity
from helper import hint
from helper import translator
from helper import url


class RecipeManager(base_manager.BaseManager):
    """ Handle recipe related actions.

    Constants:
    HINT_COOKIE -- Name of hint cookie (string).
    HINT_DELETE -- Value of delete hint cookie (string).
    HINT_EDIT -- Value of edit hint cookie (string).
    HINT_EXISTS -- Value of exists hint cookie (string).
    HINT_NAME -- Name of cookie which stores name of last changed recipe (string).
    HINT_NEW -- Value of new hint cookie (string).

    Member:
    db -- The database connection.
    hints -- List of hints which occurred during action handling (list hint).
    """

    HINT_COOKIE = 'show_hint'
    HINT_DELETE = 'delete'
    HINT_EDIT = 'edit'
    HINT_EXISTS = 'exists'
    HINT_NAME = 'last_name'
    HINT_NEW = 'new'
    HINT_NEW_EXISTS = 'new-exists'

    def __init__(self, db):
        self.db = db
        self.hints = []

    def action(self, language, indexer, static_path, image_path, id=None):
        """ Handle actions. If id is given it is assumed that an existing
         recipe is edited. Returns recipe to show. """
        _ = translator.Translator.instance(language)

        is_new = id is None
        is_edit = self.get_form('edit') is not None
        is_delete = self.get_form('delete') is not None
        is_import = self.get_form('import') is not None

        # Actions
        result = None
        if is_edit:
            categories = self.__read_categories()
            images = self.__read_images(language, static_path, image_path)
            synonyms = self.__read_synonyms()
            tags = self.__read_tags()
            urls = self.__read_urls()

            title = self.get_form('title')
            exists = is_new and recipe_entity.Recipe.title_exists(self.db, title)

            result = recipe_entity.Recipe()
            if not is_new:
                result = recipe_entity.Recipe.find_pk(self.db, id)

            manager = user_manager.UserManager(self.db)
            result.author = manager.current_user()

            result.categories = categories
            result.description = self.get_form('description')
            result.images = images
            result.info = self.get_form('info')
            result.ingredients = self.get_form('ingredients')
            result.rating = int(self.get_form('rating'))
            result.serving_size = self.get_form('serving-size')
            result.synonyms = synonyms
            result.tags = tags
            result.title = title
            result.urls = urls

            if not title:
                hint_text = _('Title must not be empty.').format(title)
                self.hints.append(hint.Hint(hint_text))
            else:
                result.save(self.db)

                # Update search index.
                scheme = indexer.scheme()
                writer = indexer.open_index(scheme)
                indexer.fill_index(writer, [result])
                indexer.close_index()

                if exists:
                    type = self.HINT_NEW_EXISTS
                elif is_new:
                    type = self.HINT_NEW
                else:
                    type = self.HINT_EDIT
                self.set_cookie(self.HINT_COOKIE, type)
                self.set_cookie(self.HINT_NAME, result.title)
                redirect(url.Url.from_path(['manage', 'recipe', str(result.id)]))

        elif is_delete:
            recipe = recipe_entity.Recipe.find_pk(self.db, id)

            # Update search index.
            scheme = indexer.scheme()
            writer = indexer.open_index(scheme)
            indexer.remove_from_index(writer, [recipe])
            indexer.close_index()

            recipe.delete(self.db)

            self.set_cookie(self.HINT_COOKIE, self.HINT_DELETE)
            self.set_cookie(self.HINT_NAME, recipe.title)
            redirect(url.Url.from_path(['manage', 'recipe']))

        elif is_new:
            result = recipe_entity.Recipe()

        #elif is_import:

        else:
            result = recipe_entity.Recipe.find_pk(self.db, id)

        self.__show_hints(language)
        return result

    def __read_categories(self):
        """ Read categories and return them. """
        categories = []
        for category_id in request.forms.getall('categories'):
            category = category_entity.Category.find_pk(self.db, category_id)
            categories.append(category)
        return categories

    def __read_images(self, language, static_path, image_root_path):
        """ Read images and return them. """
        _ = translator.Translator.instance(language)

        if not os.path.exists(static_path+image_root_path):
                os.mkdir(static_path+image_root_path)

        images = []

        # Read images from form.
        image_counter = 0
        image_path = self.get_form('image-'+str(image_counter))
        while image_path is not None:
            if image_path:
                image = image_entity.Image(path=image_path)
                images.append(image)
            image_counter += 1
            image_path = self.get_form('image-'+str(image_counter))
        image_counter = 0

        # Check images and write to file system.
        image_upload = request.files.get('new-image-'+str(image_counter))
        while image_upload is not None:
            # Check file extension.
            name, ext = os.path.splitext(image_upload.filename)
            if ext.lower() not in ('.png','.jpg','.jpeg', '.gif'):
                text = _('Extension "{}" is not an allowed image type.')\
                    .format(ext)
                self.hints.append(hint.Hint(text))
                image_counter += 1
                image_upload = request.files.get('new-image-'+str(image_counter))
                continue
            image_path = image_root_path
            image_path += name
            image_path += ext
            path_counter = 0

            # Create a unique name.
            while os.path.exists(static_path + image_path):
                image_path = image_root_path
                image_path += name
                image_path += str(path_counter)
                image_path += ext
                path_counter += 1

            # Save image and restart with next one.
            #image_upload.save(self.STATIC_PATH + image_path)
            with open(static_path + image_path, "wb") as out_file:
                out_file.write(image_upload.file.read())
            image = image_entity.Image(path=image_path)
            images.append(image)
            image_counter += 1
            image_upload = request.files.get('new-image-'+str(image_counter))

        return images

    def __read_synonyms(self):
        """ Read synonyms and return them. """
        synonyms = []
        synonym_counter = 0
        synonym_name = self.get_form('synonym-'+str(synonym_counter))
        while synonym_name is not None:
            if synonym_name:
                synonym = synonym_entity.Synonym(name=synonym_name)
                synonyms.append(synonym)
            synonym_counter += 1
            synonym_name = self.get_form('synonym-'+str(synonym_counter))
        return synonyms

    def __read_tags(self):
        """ Read tags and return them. """
        tags = []
        for tag_id in request.forms.getall('tags'):
            tag = tag_entity.Tag.find_pk(self.db, tag_id)
            tags.append(tag)
        return tags

    def __read_urls(self):
        """ Read urls and return them. """
        urls = []
        url_counter = 0
        url_url = self.get_form('url-url-'+str(url_counter))
        while url_url is not None:
            if url_url:
                url_name = self.get_form('url-name-'+str(url_counter))
                url = url_entity.Url(name=url_name, url=url_url)
                urls.append(url)
            url_counter += 1
            url_url = self.get_form('url-url-'+str(url_counter))
        return urls

    def __show_hints(self, language):
        """ Show hints if cookies are set. """
        _ = translator.Translator.instance(language)

        hint_cookie = self.get_cookie(self.HINT_COOKIE)
        name_cookie = self.get_cookie(self.HINT_NAME)
        if hint_cookie and name_cookie:
            if hint_cookie == self.HINT_NEW:
                hint_text = _('New recipe "{}" has been created.')
            elif hint_cookie == self.HINT_EDIT:
                hint_text = _('Recipe "{}" has been updated.')
            elif hint_cookie == self.HINT_NEW_EXISTS:
                hint_text = _('New recipe "{}" has been created. '
                              'A recipe with the same title already exists.')
            else:
                hint_text = _('Recipe "{}" has been removed.')
            hint_text = hint_text.format(name_cookie)
            self.hints.append(hint.Hint(hint_text))
            self.delete_cookie(self.HINT_COOKIE)
            self.delete_cookie(self.HINT_NAME)