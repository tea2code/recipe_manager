from bottle import redirect
from bottle import request
from bottle import response
from entity import category as category_entity
from entity import recipe
from helper import hint

class RecipeManager:
    """ Handle recipe related actions.

    Constants:
    HINT_COOKIE -- Name of hint cookie (string).
    HINT_DELETE -- Value of delete hint cookie (string).
    HINT_EDIT -- Value of edit hint cookie (string).
    HINT_NAME -- Name of cookie which stores name of last changed recipe (string).
    HINT_NEW -- Value of new hint cookie (string).

    Member:
    db -- The database connection.
    hints -- List of hints which occurred during action handling (list).
    """

    HINT_COOKIE = 'show_hint'
    HINT_DELETE = 'delete'
    HINT_EDIT = 'edit'
    HINT_NAME = 'last_name'
    HINT_NEW = 'new'

    def __init__(self, db):
        self.db = db
        self.hints = []

    def action(self, id=None):
        """ Handle actions. If id is given it is assumed that an existing
         recipe is edited. Returns recipe to show. """
        is_new = id is None
        is_edit = request.forms.get('edit') is not None
        is_delete = request.forms.get('delete') is not None

        # Actions
        if is_edit:
            category_id = int(request.forms.get('category'))
            category = category_entity.Category.find_pk(self.db, category_id)

            result = recipe.Recipe(id=id)
            result.category = category
            result.description = request.forms.get('description')
            result.info = request.forms.get('info')
            result.ingredients = request.forms.get('ingredients')
            result.rating = int(request.forms.get('rating'))
            result.serving_size = request.forms.get('serving-size')
            result.title = request.forms.get('title')
            result.save(self.db)

            type = self.HINT_NEW if is_new else self.HINT_EDIT
            self.__set_cookie(self.HINT_COOKIE, type)
            self.__set_cookie(self.HINT_NAME, result.title)
            redirect('/manage/recipe/'+str(result.id))
        elif is_delete:
            old_recipe = recipe.Recipe.find_pk(self.db, id)
            old_recipe.delete(self.db)

            self.__set_cookie(self.HINT_COOKIE, self.HINT_DELETE)
            self.__set_cookie(self.HINT_NAME, old_recipe.title)
            redirect('/manage/recipe')
        elif is_new:
            result = recipe.Recipe()
        else:
            result = recipe.Recipe.find_pk(self.db, id)

        # Cookies
        hint_cookie = request.get_cookie(self.HINT_COOKIE)
        name_cookie = request.get_cookie(self.HINT_NAME)
        if hint_cookie and name_cookie:
            if hint_cookie == self.HINT_NEW:
                hint_text = 'New recipe "{}" created.'.format(name_cookie)
            elif hint_cookie == self.HINT_EDIT:
                hint_text = 'Recipe "{}" updated.'.format(name_cookie)
            else:
                hint_text = 'Recipe "{}" removed.'.format(name_cookie)
            self.hints.append(hint.Hint(hint_text))
            self.__delete_cookie(self.HINT_COOKIE)
            self.__delete_cookie(self.HINT_NAME)

        return result

    def __delete_cookie(self, name,):
        """ Helper to delete all cookies with same settings. """
        response.delete_cookie(name, httponly=True, path='/')

    def __set_cookie(self, name, value):
        """ Helper to set all cookies with same settings. """
        response.set_cookie(name, value, httponly=True, path='/')