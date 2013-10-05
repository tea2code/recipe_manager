from bottle import redirect
from bottle import request
from entity import category as category_entity
from entity import recipe
from helper import hint

class RecipeManager:
    """ Handle recipe related actions.

    Member:
    db -- The database connection.
    hints -- List of hints which occurred during action handling.
    """

    def __init__(self, db):
        self.db = db
        self.hints = []

    def action(self, id=None):
        """ Handle actions. If id is given it is assumed that an existing
         recipe is edited. Returns recipe to show. """
        is_new = id is None
        is_edit = request.forms.get('edit') is not None
        is_delete = request.forms.get('delete') is not None
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
            redirect('/manage/recipe/'+str(result.id))
        elif is_delete:
            old_recipe = recipe.Recipe.find_pk(self.db, id)
            old_recipe.delete(self.db)
            redirect('/manage/recipe')
        elif is_new:
            result = recipe.Recipe()
        else:
            result = recipe.Recipe.find_pk(self.db, id)
        return result