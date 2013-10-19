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

    def fill_index(self, writer, recipes):
        """ Fill index with recipes. """
        for recipe in recipes:
            categories = ' '.join(c.name for c in recipe.categories)
            synonyms = ' '.join(s.name for s in recipe.synonyms)
            tags = ''
            for tag in recipe.tags:
                tags += tag.name + ' '
                for synonym in tag.synonyms:
                    tags += synonym.name + ' '
            writer.add_document(categories=categories,
                                description=recipe.description,
                                id=recipe.id,
                                info=recipe.info,
                                ingredients=recipe.ingredients,
                                tags=tags,
                                title=recipe.title+' '+synonyms,
                                titletags=tags+recipe.title+' '+synonyms,
                                rated=(recipe.rating is not -1))
        writer.commit()

    def open_index(self, schema):
        """ Opens an index. Returns the writer. """
        if not os.path.exists(self.index_path):
            os.mkdir(self.index_path)
            index.create_in(self.index_path, schema)
        self._index = index.open_dir(self.index_path)
        return self._index.writer()

    def remove_index(self):
        """ Removes an index. """
        if os.path.exists(self.index_path):
            shutil.rmtree(self.index_path)

    def scheme(self):
        """ Returns the scheme. """
        schema = fields.Schema(categories=fields.TEXT,
                               description=fields.TEXT,
                               id=fields.STORED,
                               info=fields.TEXT,
                               ingredients=fields.TEXT,
                               tags=fields.TEXT,
                               title=fields.TEXT,
                               titletags=fields.TEXT,
                               rated=fields.BOOLEAN)
        return schema

    def searcher(self):
        """ Returns a searcher for this index. """
        self._index = index.open_dir(self.index_path)
        return self._index.searcher()