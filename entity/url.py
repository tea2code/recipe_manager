#!/usr/bin/python
# -*- coding: utf-8 -*-


class Url:
    """ Represents an url.

    Member:
    id -- The row id or None if not yet committed (int).
    recipe_id -- The recipe id (int).
    name -- The url name (string).
    url -- The url (string).
    """

    def __init__(self, id=None, recipe_id=None, name='', url=''):
        self.id = id
        self.recipe_id = recipe_id
        self.name = name
        self.url = url

    def __str__(self):
        template = 'Url({0}, {1}, {2}, {3})'
        return template.format(self.id, self.recipe_id, self.name, self.url)

    def delete(self, db):
        """ Delete entity from database. """
        query = 'DELETE FROM urls WHERE id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all entities in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT id, recipe_id, name, url ' \
                'FROM urls ' \
                'ORDER BY name COLLATE NOCASE ASC, url COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Url.from_row(row))
        return result

    @staticmethod
    def find_pk(db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT id, recipe_id, name, url FROM urls WHERE id = ?'
        params = [id]
        return Url.__generic_find(db, query, params)

    @staticmethod
    def find_recipe(db, recipe):
        """ Find all entities by recipe in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT id, recipe_id, name, url ' \
                'FROM urls ' \
                'WHERE recipe_id = ?' \
                'ORDER BY name COLLATE NOCASE ASC, url COLLATE NOCASE ASC'
        params = [recipe.id]
        cursor = db.cursor()
        cursor.execute(query, params)
        result = []
        for row in cursor.fetchall():
            result.append(Url.from_row(row))
        return result

    @staticmethod
    def from_row(row):
        """ Create entity from given row. """
        return Url(id=row[0], recipe_id=row[1], name=row[2], url=row[3])

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write entity to database. """
        query = 'INSERT INTO urls (recipe_id, name, url) VALUES (?, ?, ?)'
        params = [self.recipe_id, self.name, self.url]
        if not self.is_new():
            query = 'UPDATE urls ' \
                    'SET recipe_id = ?, name = ?, url = ? ' \
                    'WHERE id = ?'
            params.append(self.id)
        cursor = db.cursor()
        cursor.execute(query, params)
        if self.is_new():
            self.id = cursor.lastrowid

    @staticmethod
    def __generic_find(db, query, params):
        """ Generic implementation of a find single method. Returns entity or
        None. """
        cursor = db.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return Url.from_row(row) if row else None