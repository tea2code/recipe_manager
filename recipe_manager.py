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
from action import recipe_manager
from action import tag_manager
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
    TRANSLATION_PATH = config.get('Default', 'TRANSLATION_PATH', fallback=TRANSLATION_PATH)


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


# Routes #######################################################################
# Index
@app.get('/', template='index')
def index(db):
    """ Index page. """
    language = translator.Translator.current_language(LANGUAGE)
    categories = category.Category.find_all(db)

    num_recipes = recipe.Recipe.count_all(db)
    recipes = recipe.Recipe.find_category(db, None)
    randoms = recipe.Recipe.find_random(db, RANDOM_RECIPES)
    return dict(categories=categories, recipes=recipes, randoms=randoms,
                num_recipes=num_recipes, language=language, languages=LANGUAGES)


# Category
@app.get('/category/<id:int>-<:re:.+>', template='category_list')
def category_list(db, id):
    """ Category list page. """
    language = translator.Translator.current_language(LANGUAGE)
    categories = category.Category.find_all(db)

    cat = category.Category.find_pk(db, id)
    recipes = recipe.Recipe.find_category(db, cat)
    return dict(categories=categories, category=cat, recipes=recipes,
                language=language, languages=LANGUAGES)


# Manage: Category
@app.get('/manage/categories', template='manage_categories')
@app.post('/manage/categories', template='manage_categories')
def manage_categories(db):
    """ Category managing page. """
    language = translator.Translator.current_language(LANGUAGE)

    manager = category_manager.CategoryManager(db)
    categories = manager.action(language)
    hints = manager.hints
    return dict(categories=categories, hints=hints, language=language,
                languages=LANGUAGES)


# Manage: Recipe
@app.get('/manage/recipe', template='manage_recipe')
@app.get('/manage/recipe/<id:int>', template='manage_recipe')
@app.post('/manage/recipe', template='manage_recipe')
@app.post('/manage/recipe/<id:int>', template='manage_recipe')
def manage_recipe(db, id=None):
    """ Recipe managing page. """
    language = translator.Translator.current_language(LANGUAGE)
    categories = category.Category.find_all(db)

    manager = recipe_manager.RecipeManager(db)
    rec = manager.action(language, indexer, id)
    hints = manager.hints
    tags = tag.Tag.find_all(db)
    return dict(categories=categories, recipe=rec, hints=hints, tags=tags,
                language=language, languages=LANGUAGES)


# Manage: Tag
@app.get('/manage/tags', template='manage_tags')
@app.post('/manage/tags', template='manage_tags')
def manage_tag(db):
    """ Tag managing page. """
    language = translator.Translator.current_language(LANGUAGE)
    categories = category.Category.find_all(db)

    manager = tag_manager.TagManager(db)
    tags = manager.action(language)
    hints = manager.hints
    return dict(categories=categories, tags=tags, hints=hints,
                language=language, languages=LANGUAGES)


# Recipe
@app.get('/recipe/<id:int>-<:re:.+>', template='view_recipe')
def view_recipe(db, id):
    """ Recipe view page. """
    language = translator.Translator.current_language(LANGUAGE)
    categories = category.Category.find_all(db)

    rec = recipe.Recipe.find_pk(db, id)
    return dict(categories=categories, recipe=rec, language=language,
                languages=LANGUAGES)


# Search
@app.get('/search', template='search')
@app.post('/search', template='search')
def search(db):
    """ Search page. """
    language = translator.Translator.current_language(LANGUAGE)
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
                language=language, languages=LANGUAGES)


# Statics ######################################################################
@app.get('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@app.get('/<type:re:(css|img|js)>/<file>')
@app.get('/<type:re:img/upload>/<file>')
def statics(file, type='img'):
    """ Static content like css, images and javascript. """
    return bottle.static_file(file, root=HOME+'static/'+type)


# Run ##########################################################################
app.run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)