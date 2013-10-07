class Tag:
    """ Represents a tag.

    Member:
    id -- The row id or None if not yet committed (int).
    name -- The tag name (string).
    synonym_of -- Id of parent tag or None (tag).
    synonyms -- List of synonyms. Filled only for parents (list tag).
    """

    def __init__(self, id=None, name='', synonym_of=None, synonyms=[]):
        self.id = id
        self.name = name
        self.synonym_of = synonym_of
        self.synonyms = synonyms

    def __str__(self):
        synonym_of = self.synonym_of.name if self.synonym_of else None
        template = 'Tag({0}, {1}, {2})'
        return template.format(self.id, self.name, synonym_of)

    def delete(self, db):
        """ Delete entity from database. """
        # TODO Delete recipe_has_tag.

        query = 'DELETE FROM tags WHERE id = ?'
        params = [self.id]
        if self.synonym_of is None:
            query = 'DELETE FROM tags WHERE id = ? OR synonym_of = ?'
            params.append(self.id)
        cursor = db.cursor()
        cursor.execute(query, params)

    @staticmethod
    def find_all(db):
        """ Find all parent entities in database. Returns list of found
        entities ordered by name ascending. """
        query = 'SELECT id, synonym_of, name FROM tags ' \
                'WHERE synonym_of IS NULL ' \
                'ORDER BY name COLLATE NOCASE ASC'
        cursor = db.cursor()
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            tag = Tag.from_row(row)
            tag.find_synonyms(db)
            result.append(tag)
        return result

    @staticmethod
    def find_name(db, name):
        """ Find entity by name in database. Returns found
        entity or None. """
        query = 'SELECT id, synonym_of, name FROM tags WHERE name = ?'
        params = [name]
        return Tag.__generic_find(db, query, params)

    @staticmethod
    def find_pk(db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT id, synonym_of, name FROM tags WHERE id = ?'
        params = [id]
        return Tag.__generic_find(db, query, params)

    def find_synonyms(self, db):
        """ Find synonyms of a parent. Doesn't return but add them to
        parent. """
        query = 'SELECT id, synonym_of, name FROM tags ' \
                'WHERE synonym_of = ? ' \
                'ORDER BY name COLLATE NOCASE ASC'
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)
        self.synonyms = []
        for row in cursor.fetchall():
            self.synonyms.append(Tag.from_row(row))

    @staticmethod
    def from_row(row):
        """ Create entity from given row. """
        return Tag(id=row[0], name=row[2], synonym_of=row[1])

    def is_new(self):
        """ Returns True if entity is not yet committed else False. """
        return self.id is None

    def save(self, db):
        """ Write entity to database.  """
        query = 'INSERT INTO tags (synonym_of, name) VALUES (?, ?)'
        params = [self.synonym_of, self.name]
        if not self.is_new():
            query = 'UPDATE tags SET synonym_of = ?, name = ? WHERE id = ?'
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
        tag = Tag.from_row(row) if row else None
        if tag and tag.synonym_of is None:
            tag.find_synonyms(db)
        return tag