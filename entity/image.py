class Image:
    """ Represents a image.

    Member:
    id -- The row id or None if not yet committed (int).
    recipe_id -- The recipe id (int).
    path -- The path (string).
    """

    def __init__(self, id=None, recipe_id=None, path=''):
        self.id = id
        self.recipe_id = recipe_id
        self.path = path

    def __str__(self):
        template = 'Image({0}, {1}, {2})'
        return template.format(self.id, self.recipe_id, self.path)

    def delete(self, db):
        """ Delete entity from database. """
        query = 'DELETE FROM images WHERE id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all entities in database. Returns list of found
        entities ordered by path ascending."""
        query = 'SELECT id, recipe_id, path ' \
                'FROM images ' \
                'ORDER BY id ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Image.from_row(row))
        return result

    @staticmethod
    def find_pk(db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT id, recipe_id, path FROM images WHERE id = ?'
        params = [id]
        return Image.__generic_find(db, query, params)

    @staticmethod
    def find_recipe(db, recipe):
        """ Find all entities by recipe in database. Returns list of found
        entities ordered by path ascending."""
        query = 'SELECT id, recipe_id, path ' \
                'FROM images ' \
                'WHERE recipe_id = ?' \
                'ORDER BY id ASC'
        params = [recipe.id]
        cursor = db.cursor()
        cursor.execute(query, params)
        result = []
        for row in cursor.fetchall():
            result.append(Image.from_row(row))
        return result

    @staticmethod
    def from_row(row):
        """ Create entity from given row. """
        return Image(id=row[0], recipe_id=row[1], path=row[2])

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write entity to database. """
        query = 'INSERT INTO images (recipe_id, path) VALUES (?, ?)'
        params = [self.recipe_id, self.path]
        if not self.is_new():
            query = 'UPDATE images ' \
                    'SET recipe_id = ?, path = ? ' \
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
        return Image.from_row(row) if row else None