from bottle import route, run, static_file, view

# Routes #######################################################################
@route('/')
@view('index')
def index():
    """ Index page. """
    return dict()

# Statics ######################################################################
@route('/css/<file>')
def css(file):
    """ Static content: css. """
    return static_file(file, root='static/css')

@route('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@route('/img/<file>')
def img(file):
    """ Static content: img. """
    return static_file(file, root='static/img')

@route('/js/<file>')
def js(file):
    """ Static content: js. """
    return static_file(file, root='static/js')

# Run ##########################################################################
run(host='localhost', port=8081, debug=True)