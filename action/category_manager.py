from bottle import request
from entity import category

class CategoryManager:
    """ Action handler for simple id-name-managing pages.

    Member:
    db -- The database connection.
    """

    def __init__(self, db):
        self.db = db

    def action(self):
        """ Handle action for given class name. Returns found entities. """
        # Handle actions.
        action = request.forms.get('action') or 'show'
        if action == 'new':
            name = request.forms.get('name')
            cat = category.Category(name=name)
            cat.save(self.db)
        elif action == 'edit':
            is_delete = request.forms.get('delete') is not None
            id = request.forms.get('id')
            name = request.forms.get('name')
            entity = category.Category(id, name)
            if is_delete:
                entity.delete(self.db)
            else:
                entity.save(self.db)

        # Load content.
        return category.Category.find_all(self.db)