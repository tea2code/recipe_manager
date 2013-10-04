from bottle import request

class ManageIdName:
    """ Action handler for simple id-name-managing pages.

    Member:
    db -- The database connection.
    """

    def __init__(self, db):
        self.db = db

    def handle(self, classname):
        """ Handle action for given class name. Returns found entities. """
        # Handle actions.
        action = request.forms.get('action') or 'show'
        if action == 'new':
            name = request.forms.get('name')
            cat = classname(name=name)
            cat.save(self.db)
        elif action == 'edit':
            is_delete = request.forms.get('delete') is not None
            id = request.forms.get('id')
            name = request.forms.get('name')
            cat = classname(id, name)
            if is_delete:
                cat.delete(self.db)
            else:
                cat.save(self.db)

        # Load content.
        return classname.find_all(self.db)