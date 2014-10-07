#!/usr/bin/python
# -*- coding: utf-8 -*-

import bottle
import bottle_sqlite as sqlite
import configparser
import collections
import os
import random
import sqlite3
from action import category_manager
from action import export_manager
from action import recipe_manager
from action import tag_manager
from action import user_manager
from entity import category
from entity import recipe
from entity import tag
from helper import translator
from migration import migration_manager
from search import indexer as indexer_class
from search import searcher as searcher_class


# Configuration ################################################################
config = configparser.ConfigParser()
config.read('default.config')
ADMIN_USER = config.get('Default', 'ADMIN_USER')
DB_FILE = config.get('Default', 'DB_FILE')
DEBUG = config.getboolean('Default', 'DEBUG')
ENABLE_USERS = config.getboolean('Default', 'ENABLE_USERS')
HOME = config.get('Default', 'HOME')
HOST = config.get('Default', 'HOST')
INDEX_PATH = config.get('Default', 'INDEX_PATH')
LANGUAGE = config.get('Default', 'LANGUAGE')
PORT = config.getint('Default', 'PORT')
PW_HASH_ITERATIONS = config.getint('Default', 'PW_HASH_ITERATIONS')
RANDOM_RECIPES = config.getint('Default', 'RANDOM_RECIPES')
RENEW_INDEX = config.getboolean('Default', 'RENEW_INDEX')
STATIC_PATH = config.get('Default', 'STATIC_PATH')
TRANSLATION_PATH = config.get('Default', 'TRANSLATION_PATH')

if os.path.exists('user.config'):
    config.read('user.config')
    ADMIN_USER = config.get('Default', 'ADMIN_USER', fallback=ADMIN_USER)
    DB_FILE = config.get('Default', 'DB_FILE', fallback=DB_FILE)
    DEBUG = config.getboolean('Default', 'DEBUG', fallback=DEBUG)
    ENABLE_USERS = config.getboolean('Default', 'ENABLE_USERS', fallback=ENABLE_USERS)
    HOME = config.get('Default', 'HOME', fallback=HOME)
    HOST = config.get('Default', 'HOST', fallback=HOST)
    INDEX_PATH = config.get('Default', 'INDEX_PATH', fallback=INDEX_PATH)
    LANGUAGE = config.get('Default', 'LANGUAGE', fallback=LANGUAGE)
    PORT = config.getint('Default', 'PORT', fallback=PORT)
    PW_HASH_ITERATIONS = config.getint('Default', 'PW_HASH_ITERATIONS', fallback=PW_HASH_ITERATIONS)
    RANDOM_RECIPES = config.getint('Default', 'RANDOM_RECIPES', fallback=RANDOM_RECIPES)
    RENEW_INDEX = config.getboolean('Default', 'RENEW_INDEX', fallback=RENEW_INDEX)
    STATIC_PATH = config.get('Default', 'STATIC_PATH', fallback=STATIC_PATH)
    TRANSLATION_PATH = config.get('Default', 'TRANSLATION_PATH', fallback=TRANSLATION_PATH)

IMAGE_PATH = '/img/upload/'
INDEX_PATH += '/'


# Initialization ###############################################################
app = bottle.Bottle()

# Plugins
sqlPlugin = sqlite.Plugin(dbfile=HOME+DB_FILE)
app.install(sqlPlugin)

# Migration
migration = migration_manager.MigrationManager(HOME, DB_FILE)
migration.migrate()

# Translation
LANGUAGES = collections.OrderedDict()
LANGUAGES['de_DE'] = 'Deutsch'
LANGUAGES['en_US'] = 'English'
for locale in LANGUAGES:
    translator.Translator.init(locale, TRANSLATION_PATH)

# Searching
indexer = indexer_class.Indexer(HOME+INDEX_PATH)
if RENEW_INDEX or not os.path.exists(HOME+INDEX_PATH):
    indexer.remove_index()
    scheme = indexer.scheme()
    writer = indexer.open_index(scheme)
    db = sqlite3.connect(HOME+DB_FILE)
    recipes = recipe.Recipe.find_all(db)
    db.commit()
    db.close()
    indexer.fill_index(writer, recipes)
    indexer.close_index()


# Little Helper ################################################################
def validate_user_and_language(db, enable_users):
    """ Validate the user and get the current language. """
    is_admin = False
    if enable_users:
        manager = user_manager.UserManager(db)
        manager.validate_login(PW_HASH_ITERATIONS, ADMIN_USER)
        is_admin = (manager.current_user() and
                    manager.current_user().name == ADMIN_USER)
    language = translator.Translator.current_language(LANGUAGE)
    return language, is_admin


# Routes #######################################################################
# Export: Recipe
@app.post('/export/recipe/<id:int>')
def export_recipe(db, id):
    """  """
    validate_user_and_language(db, ENABLE_USERS)

    manager = export_manager.ExportManager(db)
    return manager.action(HOME+STATIC_PATH, IMAGE_PATH, id)

# Index
@app.get('/', template='index')
def index(db):
    """ Index page. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)
    categories = category.Category.find_all(db)

    num_recipes = recipe.Recipe.count_all(db)
    recipes = recipe.Recipe.find_category(db, None)
    randoms = recipe.Recipe.find_random(db, RANDOM_RECIPES)
    return dict(categories=categories, recipes=recipes, randoms=randoms,
                num_recipes=num_recipes, language=language, languages=LANGUAGES,
                enable_users=ENABLE_USERS, is_admin=is_admin)


# Category
@app.get('/category/<id:int>-<:re:.+>', template='category_list')
def category_list(db, id):
    """ Category list page. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)
    categories = category.Category.find_all(db)

    cat = category.Category.find_pk(db, id)
    recipes = recipe.Recipe.find_category(db, cat)
    return dict(categories=categories, category=cat, recipes=recipes,
                language=language, languages=LANGUAGES, enable_users=ENABLE_USERS,
                is_admin=is_admin)


# Login
@app.get('/login', template='login')
@app.post('/login', template='login')
def login(db):
    """ Login page. """
    language, is_admin = validate_user_and_language(db, False)

    manager = user_manager.UserManager(db)
    hints = manager.login(language, PW_HASH_ITERATIONS, ADMIN_USER)
    return dict(hints=hints, language=language, languages=LANGUAGES,
                is_admin=is_admin)


# Logout
@app.get('/logout')
@app.post('/logout')
def logout(db):
    """ Login page. """
    manager = user_manager.UserManager(db)
    manager.logout()


# Manage: Category
@app.get('/manage/categories', template='manage_categories')
@app.post('/manage/categories', template='manage_categories')
def manage_categories(db):
    """ Category managing page. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)

    manager = category_manager.CategoryManager(db)
    categories = manager.action(language)
    hints = manager.hints
    return dict(categories=categories, hints=hints, language=language,
                languages=LANGUAGES, enable_users=ENABLE_USERS, is_admin=is_admin)


# Manage: Recipe
@app.get('/manage/recipe', template='manage_recipe')
@app.get('/manage/recipe/<id:int>', template='manage_recipe')
@app.post('/manage/recipe', template='manage_recipe')
@app.post('/manage/recipe/<id:int>', template='manage_recipe')
def manage_recipe(db, id=None):
    """ Recipe managing page. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)
    categories = category.Category.find_all(db)

    manager = recipe_manager.RecipeManager(db)
    rec = manager.action(language, indexer, STATIC_PATH, IMAGE_PATH, id)
    hints = manager.hints
    tags = tag.Tag.find_all(db)
    return dict(categories=categories, recipe=rec, hints=hints, tags=tags,
                language=language, languages=LANGUAGES, enable_users=ENABLE_USERS,
                is_admin=is_admin)


# Manage: Tag
@app.get('/manage/tags', template='manage_tags')
@app.post('/manage/tags', template='manage_tags')
def manage_tag(db):
    """ Tag managing page. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)
    categories = category.Category.find_all(db)

    manager = tag_manager.TagManager(db)
    tags = manager.action(language)
    hints = manager.hints
    return dict(categories=categories, tags=tags, hints=hints,
                language=language, languages=LANGUAGES, enable_users=ENABLE_USERS,
                is_admin=is_admin)


# Manage: Users
@app.get('/manage/users', template='manage_users')
@app.post('/manage/users', template='manage_users')
def manage_users(db):
    """ User managing page or personal profile. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)
    categories = category.Category.find_all(db)

    manager = user_manager.UserManager(db)
    users = manager.action(language, PW_HASH_ITERATIONS, ADMIN_USER)
    hints = manager.hints
    return dict(categories=categories, hints=hints, users=users,
                is_admin=is_admin, language=language, languages=LANGUAGES,
                enable_users=ENABLE_USERS)


# Recipe
@app.get('/recipe/<id:int>-<:re:.+>', template='view_recipe')
def view_recipe(db, id):
    """ Recipe view page. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)
    categories = category.Category.find_all(db)

    rec = recipe.Recipe.find_pk(db, id)
    return dict(categories=categories, recipe=rec, language=language,
                languages=LANGUAGES, enable_users=ENABLE_USERS, is_admin=is_admin)


# Search
@app.get('/search', template='search')
@app.post('/search', template='search')
def search(db):
    """ Search page. """
    language, is_admin = validate_user_and_language(db, ENABLE_USERS)
    categories = category.Category.find_all(db)

    query = bottle.request.forms.getunicode('q') or \
            bottle.request.query.getunicode('q') or ''
    button = bottle.request.forms.getunicode('submit') or \
             bottle.request.query.getunicode('submit') or ''
    recipes = []
    if query:
        searcher = searcher_class.Searcher(indexer)
        recipes = searcher.search(db, query)
        if button == 'lucky':
            recipes = [random.choice(recipes)]
    tags = tag.Tag.find_all(db)
    return dict(categories=categories, recipes=recipes, query=query, tags=tags,
                language=language, languages=LANGUAGES, enable_users=ENABLE_USERS,
                is_admin=is_admin)


# Statics ######################################################################
@app.get('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@app.get('/<type:re:(css|img|js)>/<file>')
@app.get('/<type:re:img/upload>/<file>')
def statics(file, type='img'):
    """ Static content like css, images and javascript. """
    return bottle.static_file(file, root=HOME+STATIC_PATH+'/'+type)


# Run ##########################################################################
try:
    import cherrypy
    server = 'cherrypy'
except ImportError:
    server = 'wsgiref'
app.run(server=server, host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)