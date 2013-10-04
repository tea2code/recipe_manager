from entity import category as category_entity

class Recipe:
    """ Represents a recipe.

    Member:
    category -- The category of this recipe (category).
    description -- The cooking description (string).
    id -- The row id or None if not yet committed (int).
    info -- Additional information (string).
    ingredients -- The ingredients (string).
    rating -- The rating (int).
    serving_size -- A short description of the serving size (string).
    title -- The title (string).
    """

    def __init__(self, category=None, description='', id=None, info='',
                 ingredients='', rating=None, serving_size='', title='' ):

        self.category = category
        self.description = description
        self.id = id
        self.info = info
        self.ingredients = ingredients
        self.rating = rating
        self.serving_size = serving_size
        self.title = title

    def __str__(self):
        template = 'Recipe({0}, {1})'
        return template.format(self.id, self.title)

    def delete(self, db):
        """ Delete entity from database. """
        # TODO Delete urls.
        # TODO Delete images.
        # TODO Delete recipe_has_tag.

        # Delete entity.
        query = 'DELETE FROM recipes WHERE id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all entities in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT * FROM recipes ORDER BY name COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Recipe.from_row(db, row))
        return result

    @staticmethod
    def find_pk(cls, db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT * FROM recipe WHERE id = ?'
        params = [id]
        return Recipe.__generic_find(db, query, params)

    @staticmethod
    def from_row(db, row):
        """ Create entity from given row. """
        category = category_entity.Category.find_pk(db, row[1])
        return Recipe(id=row[0], category=category, title=row[2],
                      serving_size=row[3], ingredients=row[4],
                      description=row[5], info=row[6], rating=row[7])

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write entity to database. """
        query = 'INSERT INTO recipe (category, description, info, ' \
                'ingredients, rating, serving_size, title) VALUES (?)'
        params = [self.category.id, self.description, self.info,
                  self.ingredients, self.rating, self.serving_size, self.title]
        if not self.is_new():
            query = 'UPDATE recipe SET category = ?, description = ?, ' \
                    'info = ?, ingredients = ?, rating = ?, serving_size = ?,' \
                    'title = ? WHERE id = ?'
            params.append(self.id)
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def __generic_find(db, query, params):
        """ Generic implementation of a find single method. Returns entity or
        None. """
        cursor = db.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return Recipe.from_row(db, row) if row else None
