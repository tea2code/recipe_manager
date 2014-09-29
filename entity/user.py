#!/usr/bin/python
# -*- coding: utf-8 -*-


class User:
    """ Represents a user.

    Member:
    id -- The row id or None if not yet committed (int).
    name -- The name of the user (string).
    pw_hash -- The password hash (string).
    salt -- The password salt (string).
    session -- The session (string).
    """

    def __init__(self, id=None, name=None, pw_hash=None, salt=None, session=None):
        self.id = id
        self.name = name
        self.pw_hash = pw_hash
        self.salt = salt
        self.session = session

    def __str__(self):
        template = 'User({0}, {1})'
        return template.format(self.id, self.name)

    @staticmethod
    def count_all(db):
        """ Returns number of all users in database. """
        query = 'SELECT COUNT(*) ' \
                'FROM users'
        cursor = db.cursor()
        cursor.execute(query)
        return cursor.fetchone()[0]

    def delete(self, db):
        """ Delete entity from database. """
        cursor = db.cursor()

        # Delete entity.
        query = 'DELETE FROM users WHERE id = ?'
        params = [self.id]
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all entities in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT id, name, pw_hash, salt, session ' \
                'FROM users ' \
                'ORDER BY name COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(User.from_row(db, row))
        return result

    @staticmethod
    def find_name(db, name):
        """ Find entity name in database. Returns found
        entity or None. """
        query = 'SELECT id, name, pw_hash, salt, session ' \
                'FROM users ' \
                'WHERE name = ?'
        params = [name]
        return User.__generic_find(db, query, params)

    @staticmethod
    def find_pk(db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT id, name, pw_hash, salt, session ' \
                'FROM users ' \
                'WHERE id = ?'
        params = [id]
        return User.__generic_find(db, query, params)

    @staticmethod
    def from_row(db, row):
        """ Create entity from given row. """
        recipe = User(id=row[0], name=row[1], pw_hash=row[2], salt=row[3],
                      session=row[4])
        return recipe

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write entity to database. """
        cursor = db.cursor()

        # Entity
        query = 'INSERT INTO users (name, pw_hash, salt, session) ' \
                'VALUES (?, ?, ?, ?)'
        params = [self.name, self.pw_hash, self.salt, self.session]
        if not self.is_new():
            query = 'UPDATE users ' \
                    'SET name = ?, pw_hash = ?, salt = ?, session = ? ' \
                    'WHERE id = ?'
            params.append(self.id)
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
        return User.from_row(db, row) if row else None