import bottle
from action import category_manager
from action import recipe_manager
from bottle.ext import sqlite
from entity import category
from entity import recipe
from migration import migration_manager

# Configuration ################################################################
DB_FILE = 'dev-db.sqlite'
DEBUG = True
HOST = '192.168.0.10'
PORT = 8081

# Initialization ###############################################################
app = bottle.Bottle()

# Plugins
sqlPlugin = sqlite.Plugin(dbfile=DB_FILE)
app.install(sqlPlugin)

# Migration
migration = migration_manager.MigrationManager(DB_FILE)
migration.migrate()

# Routes #######################################################################
@app.get('/', template='index')
def index(db):
    """ Index page. """
    categories = category.Category.find_all(db)
    return dict(categories=categories)

@app.get('/category/<id:int>-<:re:.+>', template='category_list')
def category_list(db, id):
    """ Category list page. """
    cat = category.Category.find_pk(db, id)
    recipes = recipe.Recipe.find_category(db, cat)
    categories = category.Category.find_all(db)
    return dict(categories=categories, category=cat, recipes=recipes)

@app.get('/recipe/<id:int>-<:re:.+>', template='view_recipe')
def view_recipe(db, id):
    """ Recipe view page. """
    rec = recipe.Recipe.find_pk(db, id)
    categories = category.Category.find_all(db)
    return dict(categories=categories,  recipe=rec)

@app.get('/manage/categories', template='manage_categories')
@app.post('/manage/categories', template='manage_categories')
def manage_categories(db):
    """ Category managing page. """
    manager = category_manager.CategoryManager(db)
    categories = manager.action()
    hints = manager.hints
    return dict(categories=categories, hints=hints)

@app.get('/manage/recipe', template='manage_recipe')
@app.get('/manage/recipe/<id:int>', template='manage_recipe')
@app.post('/manage/recipe', template='manage_recipe')
@app.post('/manage/recipe/<id:int>', template='manage_recipe')
def manage_recipe(db, id=None):
    """ Recipe managing page. """
    categories = category.Category.find_all(db)
    manager = recipe_manager.RecipeManager(db)
    recipe = manager.action(id)
    hints = manager.hints
    return dict(categories=categories, recipe=recipe, hints=hints)

# Statics ######################################################################
@app.get('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@app.get('/<type:re:(css|img|js)>/<file>')
def statics(file, type='img'):
    """ Static content like css, images and javascript. """
    return bottle.static_file(file, root='static/'+type)

# Run ##########################################################################
app.run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)