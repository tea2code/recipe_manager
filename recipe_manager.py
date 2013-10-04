import bottle
from action import category_manager
from bottle.ext import sqlite
from entity import category
from migration import migration_manager

# Configuration ################################################################
DB_FILE = 'dev-db.sqlite'
DEBUG = True
HOST = '192.168.0.10'
PORT = 8081

# Initialization ###############################################################
app = bottle.Bottle()
sqlPlugin = sqlite.Plugin(dbfile=DB_FILE)
app.install(sqlPlugin)

migration = migration_manager.MigrationManager(DB_FILE)
migration.migrate()

# Routes #######################################################################
@app.get('/', template='index')
def index(db):
    """ Index page. """
    return dict(categories=category.Category.find_all(db))

@app.get('/manage/categories', template='manage_categories')
@app.post('/manage/categories', template='manage_categories')
def manage_categories(db):
    """ Category managing page. """
    manager = category_manager.CategoryManager(db)
    categories = manager.action()
    return dict(categories=categories)

# Statics ######################################################################
@app.get('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@app.get('/<type:re:(css|img|js)>/<file>')
def statics(file, type='img'):
    """ Static content like css, images and javascript. """
    return bottle.static_file(file, root='static/'+type)

# Run ##########################################################################
app.run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)