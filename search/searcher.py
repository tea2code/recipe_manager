#!/usr/bin/python
# -*- coding: utf-8 -*-

from entity import recipe as recipe_entity
from whoosh import qparser

class Searcher:
    """ Searcher class.

    Constants:
    DEFAULT_FIELD -- Name of the default field to search (string).

    Member:
    _indexer -- The indexer (indexer).
    """

    DEFAULT_FIELD = 'titletags'

    def __init__(self, indexer):
        self._indexer = indexer

    def search(self, db, query_text):
        """ Search this query. Returns found recipes. """
        parser = qparser.QueryParser(self.DEFAULT_FIELD, self._indexer.scheme())
        query = parser.parse(query_text)
        recipes = []
        with self._indexer.searcher() as searcher:
            results = searcher.search(query, limit=None)
            if not results:
                return []
            for hit in results:
                recipe = recipe_entity.Recipe.find_pk(db, hit['id'])
                recipes.append(recipe)
        return recipes