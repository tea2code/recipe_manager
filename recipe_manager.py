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
@app.route('/', template='index')
def index():
    """ Index page. """
    return dict()

@app.route('/manage/categories', template='manage_id_name')
@app.route('/manage/categories/<action>', template='manage_id_name', method='POST')
def manage_categories(db, action='show'):
    """ Category managing page. """
    manager = manage_id_name.ManageIdName(db)
    categories = manager.handle(action, category.Category)
    return dict(path='categories', name='Category', existing=categories,
                title='Categories')

@app.route('/manage/languages', template='manage_id_name')
@app.route('/manage/languages/<action>', template='manage_id_name', method='POST')
def manage_languages(db, action='show'):
    """ Language managing page. """
    manager = manage_id_name.ManageIdName(db)
    languages = manager.handle(action, language.Language)
    return dict(path='languages', name='Language', existing=languages,
                title='Languages')

# Statics ######################################################################
@app.route('/css/<file>')
def css(file):
    """ Static content: css. """
    return bottle.static_file(file, root='static/css')

@app.route('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@app.route('/img/<file>')
def img(file):
    """ Static content: img. """
    return bottle.static_file(file, root='static/img')

@app.route('/js/<file>')
def js(file):
    """ Static content: js. """
    return bottle.static_file(file, root='static/js')

# Run ##########################################################################
app.run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)