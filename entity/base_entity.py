from abc import ABCMeta, abstractclassmethod

class BaseEntity(metaclass=ABCMeta):
    """ Base class for entities.

    Constants:
    TABLE -- The table name in the database (string). Must be set by sub class.

    Member:
    id -- The row id or None if not yet committed (int).
    """

    def __init__(self, id=None):
        """ Should be called by sub classes. """
        self.id = id

    def delete(self, db):
        """ Delete entity from database. """
        query = 'DELETE FROM {0} WHERE id = ?'.format(self.TABLE)
        params = [self.id]
        cursor = db.cursor()
        cursor.execute(query, params)

    @classmethod
    def find_pk(cls, db, id):
        """ Find entity by primary key aka row id in database. Returns found
        entity or None. """
        query = 'SELECT * FROM {0} WHERE id = ?'.format(cls.TABLE)
        params = [id]
        return BaseEntity.generic_find(db, query, params)

    def is_new(self):
        """ Returns True if category is not yet committed else False. """
        return self.id is None

    @staticmethod
    def generic_find(db, query, params):
        """ Generic implementation of a find single method. Returns entity or
        None. """
        cursor = db.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return BaseEntity.entity_from_row(row) if row else None

    @staticmethod
    @abstractclassmethod
    def entity_from_row(row):
        """ Implement in sub classes. Should accept a *-row from database and
         create a entity from it. """
        pass

    def _save(self, db, params):
        """ Write entity to database. """
        query = 'INSERT INTO {0} (name) VALUES (?)'.format(self.TABLE)
        if not self.is_new():
            query = 'UPDATE {0} SET name = ? WHERE id = ?'.format(self.TABLE)
        cursor = db.cursor()
        cursor.execute(query, params)