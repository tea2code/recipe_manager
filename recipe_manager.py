import bottle
from action import manage_id_name
from bottle.ext import sqlite
from entity import category, language

# Configuration ################################################################
DB_FILE = 'dev-db.sqlite'
DEBUG = True
HOST = 'localhost'
PORT = 8081

# Initialization ###############################################################
app = bottle.Bottle()
sqlPlugin = sqlite.Plugin(dbfile=DB_FILE)
app.install(sqlPlugin)

# Routes #######################################################################
@app.get('/', template='index')
def index():
    """ Index page. """
    return dict()

@app.get('/manage/categories', template='manage_id_name')
@app.post('/manage/categories', template='manage_id_name')
def manage_categories(db):
    """ Category managing page. """
    manager = manage_id_name.ManageIdName(db)
    categories = manager.handle(category.Category)
    return dict(path='categories', name='Category', existing=categories,
                title='Categories')

@app.get('/manage/languages', template='manage_id_name')
@app.post('/manage/languages', template='manage_id_name')
def manage_languages(db):
    """ Language managing page. """
    manager = manage_id_name.ManageIdName(db)
    languages = manager.handle(language.Language)
    return dict(path='languages', name='Language', existing=languages,
                title='Languages')

# Statics ######################################################################
@app.get('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@app.get('/<type:re:(css|img|js)>/<file>')
def statics(file, type='img'):
    """ Static content like css, images and javascript. """
    return bottle.static_file(file, root='static/'+type)

# Run ##########################################################################
app.run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)