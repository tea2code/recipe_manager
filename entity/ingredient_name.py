from entity import base_entity
from entity import ingredient
from entity import language

class IngredientName(base_entity.BaseEntity):
    """ Represents an ingredient name.

    Member:
    language -- The language (language).
    name -- The ingredient name (string).
    parent -- The ingredient (ingredient).
    """

    TABLE = 'ingredient_names'

    def __init__(self, id=None, name=''):
        super().__init__(id)
        self.name = name

    def __str__(self):
        template = 'Category({0}, {1})'
        return template.format(self.id, self.name)

    @classmethod
    def find_all(cls, db):
        """ Find all categories in database. Returns list of found
        categories ordered by name ascending."""
        query = 'SELECT id, name FROM {0} ORDER BY name COLLATE NOCASE ASC'
        query = query.format(cls.TABLE)
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(cls.entity_from_row(row))
        return result

    @classmethod
    def find_name(cls, db, name):
        """ Find category by name in database. Returns found
        category or None. """
        query = 'SELECT id, name FROM {0} WHERE name = ?'.format(cls.TABLE)
        params = [name]
        return super().generic_find(db, query, params)

    def save(self, db):
        """ Write category to database. """
        params = [self.name]
        if not self.is_new():
            params = [self.name, self.id]
        super()._save(db, params)

    @staticmethod
    def entity_from_row(row):
        return Category(row[0], row[1])