class Language:
    """ Represents a language.

    Member:
    id -- The row id or None if not yet committed (int).
    name -- The language name (string).
    """

    def __init__(self, id=None, name=''):
        self.id = id
        self.name = name

    def __str__(self):
        template = 'Language({0}, {1})'
        return template.format(self.id, self.name)

    def delete(self, db):
        """ Delete language from database. """
        query = 'DELETE FROM languages WHERE id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def findall(db):
        """ Find all languages in database. Returns list of found
        languages ordered by name ascending."""
        query = 'SELECT id, name FROM languages ORDER BY name COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Language(row[0], row[1]))
        return result

    @staticmethod
    def findname(db, name):
        """ Find language by name in database. Returns found
        language or None. """
        query = 'SELECT id, name FROM languages WHERE name = ?'
        params = [name]
        return Language.__generic_find(db, query, params)

    @staticmethod
    def findpk(db, id):
        """ Find language by primary key aka row id in database. Returns found
        languages or None. """
        query = 'SELECT id, name FROM languages WHERE id = ?'
        params = [id]
        return Language.__generic_find(db, query, params)

    def is_new(self):
        """ Returns True if language is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write language to database. """
        query = 'INSERT INTO languages (name) VALUES (?)'
        params = [self.name]
        if not self.is_new():
            query = 'UPDATE languages SET name = ? WHERE id = ?'
            params = [self.name, self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def __generic_find(db, query, params):
        """ Generic implementation of a find single method. Returns language or
        None. """
        cursor = db.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return Language(row[0], row[1]) if row else None