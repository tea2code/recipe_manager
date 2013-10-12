from entity import configuration as config_entity
from entity import tag as tag_entity
from migration import tags as tag_lists

import os
import shutil
import sqlite3
import sys

class MigrationManager:
    """ Checks current version and migrates if necessary.

    Constants:
    CONFIG_VERSION -- The version name in configuration table (string).
    EMPTY_DB_FILE -- Name of empty database file (string).

    Member:
    db_file -- Path to sqlite database file.
    """

    CONFIG_VERSION = 'version'
    EMPTY_DB_FILE = 'empty-db.sqlite'

    def __init__(self, db_file):
        self.db_file = db_file

    def migrate(self):
        """ Executes checks and migrates if necessary. Sub functions should
        always commit changes in the database. """
        # Version 1
        self.__create_db()
        db = sqlite3.connect(self.db_file)

        # Version 1 -> 2
        if self.__is_version(db, 1):
            self.__create_tags(db, tag_lists.tags_001)
            self.__update_version(db, 2)

        # Version 2 -> 3
        if self.__is_version(db, 2):
            self.__create_tags(db, tag_lists.tags_002)
            self.__update_version(db, 3)

        # Finished
        db.close()

    def __create_db(self):
        """ Create database file if not existing. """
        if not os.path.exists(self.db_file):
            shutil.copy(self.EMPTY_DB_FILE, self.db_file)

    def __create_tags(self, db, tags):
        """ Create initial set of German and English tags. """
        for tag_names in tags:
            first = True
            parent_id = None
            for tag_name in tag_names:
                tag = tag_entity.Tag(name=tag_name, synonym_of=parent_id)
                try:
                    tag.save(db)
                except sqlite3.IntegrityError:
                    print('{} in [{}]'.format(tag_name, ', '.join(tag_names)))
                    sys.exit(80085)
                if first:
                    parent_id = tag.id
                    first = False
        db.commit()

    def __is_version(self, db, version):
        """ Checks version in configuration table. """
        config = config_entity.Configuration.find_name(db, self.CONFIG_VERSION)
        return int(config.value) is version

    def __update_version(self, db, version):
        """ Sets version in configuration table to given value. """
        config = config_entity.Configuration.find_name(db, self.CONFIG_VERSION)
        config.value = str(version)
        config.save(db)
        db.commit()