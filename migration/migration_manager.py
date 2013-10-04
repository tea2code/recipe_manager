import os
import shutil

class MigrationManager:
    """ Checks current version and migrates if necessary.

    Member:
    db_file -- Path to sqlite database file.
    """

    EMPTY_DB_FILE = 'empty-db.sqlite'

    def __init__(self, db_file):
        self.db_file = db_file

    def migrate(self):
        """ Executes checks and migrates if necessary. """
        self.__create_db()

    def __create_db(self):
        """ Create database file if not existing. """
        if not os.path.exists(self.db_file):
            shutil.copy(self.EMPTY_DB_FILE, self.db_file)