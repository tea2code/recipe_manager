import bottle
from bottle.ext import sqlite
from entity import category

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

@app.route('/manage/categories', template='manage_categories')
@app.route('/manage/categories/<action>', template='manage_categories', method='POST')
def manage_categories(db, action='show'):
    """ Category managing page. """
    # Handle actions.
    if action == 'new':
        name = bottle.request.forms.get('name')
        cat = category.Category(name=name)
        cat.save(db)
    elif action == 'edit':
        is_delete = bottle.request.forms.get('delete') is not None
        id = bottle.request.forms.get('id')
        name = bottle.request.forms.get('name')
        cat = category.Category(id, name)
        if is_delete:
            cat.delete(db)
        else:
            cat.save(db)

    # Load content.
    categories = category.Category.findall(db)
    return dict(categories=categories)

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