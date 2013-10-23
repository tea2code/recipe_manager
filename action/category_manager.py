#!/usr/bin/python
# -*- coding: utf-8 -*-

from action import base_manager
from entity import category
from helper import hint

class CategoryManager(base_manager.BaseManager):
    """ Handle category related actions.

    Member:
    db -- The database connection.
    hints -- List of hints which occurred during action handling (list hint).
    """

    def __init__(self, db):
        self.db = db
        self.hints = []

    def action(self):
        """ Handle action for given class name. Returns found entities. """
        # Handle actions.
        action = self.get_form('action') or 'show'

        if action == 'new':
            name = self.get_form('name')
            if not self.__name_exists(name):
                cat = category.Category(name=name)
                cat.save(self.db)
                hint_text = 'New category "{}" has been created.'.format(name)
                self.hints.append(hint.Hint(hint_text))

        elif action == 'edit':
            is_delete = self.get_form('delete') is not None
            id = int(self.get_form('id'))
            name = self.get_form('name')
            entity = category.Category.find_pk(self.db, id)
            entity.name = name

            if is_delete:
                entity.delete(self.db)
                hint_text = 'Category "{}" has been removed.'.format(name)
                self.hints.append(hint.Hint(hint_text))
            else:
                if not self.__name_exists(name):
                    entity.save(self.db)
                    hint_text = 'Category "{}" has been updated.'.format(name)
                    self.hints.append(hint.Hint(hint_text))

        # Load content.
        return category.Category.find_all(self.db)

    def __name_exists(self, name):
        """ Check if name already exists. If so returns True and adds hint. """
        exists = category.Category.name_exists(self.db, name)
        if exists:
            hint_text = 'Category "{}" already exists.'.format(name)
            self.hints.append(hint.Hint(hint_text))
        return exists