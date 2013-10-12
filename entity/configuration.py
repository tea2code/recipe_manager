class Configuration:
    """ Represents a configuration.

    Member:
    id -- The row id or None if not yet committed (int).
    name -- The configuration name (string).
    value -- The configuration value (string).
    """

    def __init__(self, id=None, name='', value=''):
        self.id = id
        self.name = name
        self.value = value

    def __str__(self):
        template = 'Configuration({0}, {1}, {2})'
        return template.format(self.id, self.name, self.value)

    def delete(self, db):
        """ Delete entity from database. """
        query = 'DELETE FROM configurations WHERE id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all entities in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT id, name, value FROM configurations ORDER BY name COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Configuration.from_row(row))
        return result

    @staticmethod
    def find_name(db, name):
        """ Find entity by name in database. Returns found
        entity or None. """
        query = 'SELECT id, name, value FROM configurations WHERE name = ?'
        params = [name]
        return Configuration.__generic_find(db, query, params)

    @staticmethod
    def find_pk(db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT id, name, value FROM configurations WHERE id = ?'
        params = [id]
        return Configuration.__generic_find(db, query, params)

    @staticmethod
    def from_row(row):
        """ Create entity from given row. """
        return Configuration(id=row[0], name=row[1], value=row[2])

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write entity to database. """
        query = 'INSERT INTO configurations (name) VALUES (?, ?)'
        params = [self.name, self.value]
        if not self.is_new():
            query = 'UPDATE configurations SET name = ?, value = ? WHERE id = ?'
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
        return Configuration.from_row(row) if row else None