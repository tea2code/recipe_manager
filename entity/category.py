#!/usr/bin/python
# -*- coding: utf-8 -*-

class Category:
    """ Represents a category.

    Member:
    id -- The row id or None if not yet committed (int).
    name -- The category name (string).
    """

    def __init__(self, id=None, name=''):
        self.id = id
        self.name = name

    def __str__(self):
        template = 'Category({0}, {1})'
        return template.format(self.id, self.name)

    def delete(self, db):
        """ Delete entity from database. """
        # TODO Delete/move recipe?

        query = 'DELETE FROM categories WHERE id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all entities in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT id, name ' \
                'FROM categories ' \
                'ORDER BY name COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Category.from_row(row))
        return result

    @staticmethod
    def find_name(db, name):
        """ Find entity by name in database. Returns found
        entity or None. """
        query = 'SELECT id, name FROM categories WHERE name = ?'
        params = [name]
        return Category.__generic_find(db, query, params)

    @staticmethod
    def find_pk(db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT id, name FROM categories WHERE id = ?'
        params = [id]
        return Category.__generic_find(db, query, params)

    @staticmethod
    def find_recipe(db, recipe):
        """ Find entities by recipe. Returns list of found entities ordered by
        name ascending. """
        query = 'SELECT c.id, c.name ' \
                'FROM categories c, recipe_has_category rhc ' \
                'WHERE c.id = rhc.category_id ' \
                'AND rhc.recipe_id = ? ' \
                'ORDER BY name COLLATE NOCASE ASC'
        params = [recipe.id]
        cursor = db.cursor()
        cursor.execute(query, params)
        result = []
        for row in cursor.fetchall():
            result.append(Category.from_row(row))
        return result

    @staticmethod
    def from_row(row):
        """ Create entity from given row. """
        return Category(id=row[0], name=row[1])

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    @staticmethod
    def name_exists(db, name):
        """ Checks if a name already exists. Returns True if exists else
        False. """
        query = 'SELECT EXISTS(SELECT 1 FROM categories WHERE name = ? LIMIT 1)'
        params = [name]
        cursor = db.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()[0] is 1

    def save(self, db):
        """ Write entity to database. """
        query = 'INSERT INTO categories (name) VALUES (?)'
        params = [self.name]
        if not self.is_new():
            query = 'UPDATE categories SET name = ? WHERE id = ?'
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
        return Category.from_row(row) if row else None