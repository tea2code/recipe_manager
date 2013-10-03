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
        """ Delete category from database. """
        query = 'DELETE FROM categories WHERE id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def findall(db):
        """ Find all Categories in database. Returns list of found
        Categories ordered by name ascending."""
        query = 'SELECT id, name FROM categories ORDER BY name ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Category(row[0], row[1]))
        return result

    @staticmethod
    def findname(db, name):
        """ Find Category by name in database. Returns found
        Category or None. """
        query = 'SELECT id, name FROM categories WHERE name = ?'
        params = [name]
        return Category.__generic_find(db, query, params)

    @staticmethod
    def findpk(db, id):
        """ Find Category by primary key aka row id in database. Returns found
        Category or None. """
        query = 'SELECT id, name FROM categories WHERE id = ?'
        params = [id]
        return Category.__generic_find(db, query, params)

    def is_new(self):
        """ Returns True if Category is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write Category to database. """
        query = 'INSERT INTO categories (name) VALUES (?)'
        params = [self.name]
        if not self.is_new():
            query = 'UPDATE categories SET name = ? WHERE id = ?'
            params = [self.name, self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def __generic_find(db, query, params):
        """ Generic implementation of a find single method. Returns Category or
        None. """
        cursor = db.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return Category(row[0], row[1]) if row else None