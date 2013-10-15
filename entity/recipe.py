from entity import category as category_entity
from entity import image as image_entity
from entity import synonym as synonym_entity
from entity import tag as tag_entity
from entity import url as url_entity

import os

class Recipe:
    """ Represents a recipe.

    Member:
    categories -- List of category of this recipe (list category).
    description -- The cooking description (string).
    id -- The row id or None if not yet committed (int).
    images -- List of images (list image).
    info -- Additional information (string).
    ingredients -- The ingredients (string).
    rating -- The rating (int).
    serving_size -- A short description of the serving size (string).
    synonyms -- List of synonyms for the title (list synonym).
    tags -- List of tags (list tag).
    title -- The title (string).
    urls -- List of urls (list url).
    """

    def __init__(self, categories=[], description='', id=None, info='',
                 ingredients='', rating=None, serving_size='', title='',
                 tags=[], urls=[], synonyms=[], images=[]):
        self.categories = categories
        self.description = description
        self.id = id
        self.images = images
        self.info = info
        self.ingredients = ingredients
        self.rating = rating
        self.serving_size = serving_size
        self.synonyms = synonyms
        self.tags = tags
        self.title = title
        self.urls = urls

    def __str__(self):
        template = 'Recipe({0}, {1})'
        return template.format(self.id, self.title)

    @staticmethod
    def count_all(db):
        """ Returns number of all recipes in database. """
        query = 'SELECT COUNT(*) ' \
                'FROM recipes'
        cursor = db.cursor()
        cursor.execute(query)
        return cursor.fetchone()[0]

    def delete(self, db):
        """ Delete entity from database. """
        cursor = db.cursor()

        # Delete images.
        self.__delete_images(db, force=True)

        # Delete recipe_has_category.
        self.__delete_recipe_has_category(db)

        # Delete recipe_has_tag.
        self.__delete_recipe_has_tag(db)

        # Delete synonyms.
        self.__delete_synonyms(db)

        # Delete urls.
        self.__delete_urls(db)

        # Delete entity.
        query = 'DELETE FROM recipes WHERE id = ?'
        params = [self.id]
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all entities in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT description, id, info, ingredients, ' \
                'rating, serving_size, title ' \
                'FROM recipes ' \
                'ORDER BY title COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            result.append(Recipe.from_row(db, row))
        return result

    @staticmethod
    def find_category(db, category):
        """ Find entities by category in database or entities without category
        if category is None. Returns list of found
        entities ordered by name ascending. """
        query = 'SELECT description, id, info, ingredients, ' \
                'rating, serving_size, title ' \
                'FROM recipes ' \
                'WHERE id NOT IN (SELECT recipe_id FROM recipe_has_category) ' \
                'ORDER BY title COLLATE NOCASE ASC'
        params = []
        if category:
            query = 'SELECT r.description, r.id, r.info, r.ingredients, ' \
                    'r.rating, r.serving_size, r.title ' \
                    'FROM recipes r, recipe_has_category rhc ' \
                    'WHERE rhc.recipe_id = r.id ' \
                    'AND rhc.category_id = ? ' \
                    'ORDER BY title COLLATE NOCASE ASC'
            params = [category.id]
        cursor = db.cursor()
        cursor.execute(query, params)
        result = []
        for row in cursor.fetchall():
            result.append(Recipe.from_row(db, row))
        return result

    @staticmethod
    def find_pk(db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT description, id, info, ingredients, rating, ' \
                'serving_size, title ' \
                'FROM recipes ' \
                'WHERE id = ?'
        params = [id]
        return Recipe.__generic_find(db, query, params)

    @staticmethod
    def find_random(db, num):
        """ Find random entities in database. Returns list of found
        entities ordered by name ascending."""
        query = 'SELECT description, id, info, ingredients, ' \
                'rating, serving_size, title ' \
                'FROM recipes ' \
                'ORDER BY RANDOM() ' \
                'LIMIT ?'
        params = [num]
        cursor = db.cursor()
        cursor.execute(query, params)
        result = []
        for row in cursor.fetchall():
            result.append(Recipe.from_row(db, row))
        return result

    @staticmethod
    def from_row(db, row):
        """ Create entity from given row. """
        recipe = Recipe(description=row[0], id=row[1], info=row[2],
                        ingredients=row[3], rating=row[4], serving_size=row[5],
                        title=row[6])
        recipe.categories = category_entity.Category.find_recipe(db, recipe)
        recipe.images = image_entity.Image.find_recipe(db, recipe)
        recipe.synonyms = synonym_entity.Synonym.find_recipe(db, recipe)
        recipe.tags = tag_entity.Tag.find_recipe(db, recipe)
        recipe.urls = url_entity.Url.find_recipe(db, recipe)
        return recipe

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write entity to database. """
        cursor = db.cursor()

        # Entity
        query = 'INSERT INTO recipes (description, info, ' \
                'ingredients, rating, serving_size, title) ' \
                'VALUES (?, ?, ?, ?, ?, ?)'
        params = [self.description, self.info,
                  self.ingredients, self.rating, self.serving_size, self.title]
        if not self.is_new():
            query = 'UPDATE recipes ' \
                    'SET description = ?, info = ?, ingredients = ?, ' \
                    'rating = ?, serving_size = ?, title = ? ' \
                    'WHERE id = ?'
            params.append(self.id)
        cursor.execute(query, params)
        if self.is_new():
            self.id = cursor.lastrowid

        # Images
        self.__delete_images(db)
        for image in self.images:
            image.recipe_id = self.id
            image.save(db)

        # Categories
        self.__delete_recipe_has_category(db)
        for category in self.categories:
            query = 'INSERT INTO recipe_has_category (recipe_id, category_id) ' \
                    'VALUES (?, ?)'
            params = [self.id, category.id]
            cursor.execute(query, params)

        # Synonyms
        self.__delete_synonyms(db)
        for synonym in self.synonyms:
            synonym.recipe_id = self.id
            synonym.save(db)

        # Tags
        self.__delete_recipe_has_tag(db)
        for tag in self.tags:
            query = 'INSERT INTO recipe_has_tag (recipe_id, tag_id) ' \
                    'VALUES (?, ?)'
            params = [self.id, tag.id]
            cursor.execute(query, params)

        # Urls
        self.__delete_urls(db)
        for url in self.urls:
            url.recipe_id = self.id
            url.save(db)

    def __delete_images(self, db, force=False):
        """ Deletes entries in images and from file system. If force is set to
        True files will always be removed. """
        # Files (load currently stored from database, ignore possible new ones
        # in self.images)
        image_pathes = [image.path for image in self.images]
        images = image_entity.Image.find_recipe(db, self)
        for image in images:
            if image.path not in image_pathes or force:
                os.remove('static'+image.path)

        # Database
        query = 'DELETE FROM images WHERE recipe_id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    def __delete_recipe_has_category(self, db):
        """ Deletes entries in recipe_has_tag. """
        query = 'DELETE FROM recipe_has_category WHERE recipe_id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    def __delete_recipe_has_tag(self, db):
        """ Deletes entries in recipe_has_tag. """
        query = 'DELETE FROM recipe_has_tag WHERE recipe_id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    def __delete_synonyms(self, db):
        """ Deletes entries in synonyms. """
        query = 'DELETE FROM synonyms WHERE recipe_id = ?'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    def __delete_urls(self, db):
        """ Deletes entries in urls. """
        query = 'DELETE FROM urls WHERE recipe_id = ?'
        params = [self.id]
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
