#!/usr/bin/python
# -*- coding: utf-8 -*-

from whoosh import fields
from whoosh import index

import os
import shutil


class Indexer:
    """ Class handles creating the search index.

    Member:
    index_path -- The index path (string).
    _index -- The index object (whoosh.index).
    """

    def __init__(self, index_path):
        self._index = None
        self.index_path = index_path

    def close_index(self):
        """ Closes the index. """
        self._index.close()

    @staticmethod
    def fill_index(writer, recipes):
        """ Fill index with recipes. If a recipe already exists it is
        updated. """
        for recipe in recipes:
            author = recipe.author.name if recipe.author else ''
            categories = ' '.join(c.name for c in recipe.categories)
            synonyms = ' '.join(s.name for s in recipe.synonyms)
            tags = ''
            for tag in recipe.tags:
                tags += tag.name + ' '
                for synonym in tag.synonyms:
                    tags += synonym.name + ' '
            writer.update_document(category=categories,
                                   description=recipe.description,
                                   id=str(recipe.id),
                                   info=recipe.info,
                                   ingredients=recipe.ingredients,
                                   tags=tags,
                                   title=recipe.title+' '+synonyms,
                                   titletags=tags+recipe.title+' '+synonyms,
                                   rated=(recipe.rating is not -1),
                                   author=author)
        writer.commit()

    def open_index(self, schema):
        """ Opens an index. Returns the writer. """
        if not os.path.exists(self.index_path):
            os.mkdir(self.index_path)
            index.create_in(self.index_path, schema)
        self._index = index.open_dir(self.index_path)
        return self._index.writer()

    @staticmethod
    def remove_from_index(writer, recipes):
        """ Remove recipes from index. """
        for recipe in recipes:
            writer.delete_by_term("id", str(recipe.id))
        writer.commit()

    def remove_index(self):
        """ Removes an index. """
        if os.path.exists(self.index_path):
            shutil.rmtree(self.index_path)

    @staticmethod
    def scheme():
        """ Returns the scheme. """
        schema = fields.Schema(category=fields.TEXT,
                               description=fields.TEXT,
                               id=fields.ID(stored=True, unique=True),
                               info=fields.TEXT,
                               ingredients=fields.TEXT,
                               tags=fields.TEXT,
                               title=fields.TEXT,
                               titletags=fields.TEXT,
                               rated=fields.BOOLEAN,
                               author=fields.TEXT)
        return schema

    def searcher(self):
        """ Returns a searcher for this index. """
        self._index = index.open_dir(self.index_path)
        return self._index.searcher()