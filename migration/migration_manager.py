from entity import tag as tag_entity
from migration import tags as tag_lists

import os
import shutil
import sqlite3

class MigrationManager:
    """ Checks current version and migrates if necessary.

    Member:
    db -- The database connection.
    db_file -- Path to sqlite database file.
    """

    EMPTY_DB_FILE = 'empty-db.sqlite'

    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file)
        self.db_file = db_file

    def migrate(self):
        """ Executes checks and migrates if necessary. """
        self.__create_db()
        #self.__001_create_tags()

    def __001_create_tags(self):
        """ Create initial set of German and English tags. """
        # TODO Check for database version.

        # Save
        tags = tag_lists.tags_001
        for tag_names in tags:
            first = True
            parent_id = None
            for tag_name in tag_names:
                tag = tag_entity.Tag(name=tag_name[0], synonym_of=parent_id)
                tag.save(self.db)
                if not first:
                    parent_id = tag.id
                    first = False

    def __create_db(self):
        """ Create database file if not existing. """
        if not os.path.exists(self.db_file):
            shutil.copy(self.EMPTY_DB_FILE, self.db_file)