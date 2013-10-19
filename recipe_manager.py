#!/usr/bin/python
# -*- coding: utf-8 -*-

import bottle
from action import category_manager
from action import recipe_manager
from action import tag_manager
from bottle.ext import sqlite
from entity import category
from entity import recipe
from entity import tag
from migration import migration_manager
from search import indexer as indexer_class
from search import searcher as searcher_class
from helper import browser
import sqlite3

# Configuration ################################################################
DB_FILE = 'db.sqlite'
DEBUG = True
HOST = '192.168.0.10'
INDEX_PATH = 'index/'
PORT = 8081
RANDOM_RECIPES = 3

# Initialization ###############################################################
app = bottle.Bottle()

# Plugins
sqlPlugin = sqlite.Plugin(dbfile=DB_FILE)
app.install(sqlPlugin)

# Migration
migration = migration_manager.MigrationManager(DB_FILE)
migration.migrate()

# Searching
def init_search():
    indexer = indexer_class.Indexer(INDEX_PATH)
    indexer.remove_index()
    scheme = indexer.scheme()
    writer = indexer.open_index(scheme)
    db = sqlite3.connect(DB_FILE)
    recipes = recipe.Recipe.find_all(db)
    db.commit()
    db.close()
    indexer.fill_index(writer, recipes)
    indexer.close_index()
init_search()

# Routes #######################################################################
# Index
@app.get('/', template='index')
def index(db):
    """ Index page. """
    num_recipes = recipe.Recipe.count_all(db)
    recipes = recipe.Recipe.find_category(db, None)
    randoms = recipe.Recipe.find_random(db, RANDOM_RECIPES)
    categories = category.Category.find_all(db)
    return dict(categories=categories, recipes=recipes, randoms=randoms,
                num_recipes=num_recipes)

# Category
@app.get('/category/<id:int>-<:re:.+>', template='category_list')
def category_list(db, id):
    """ Category list page. """
    cat = category.Category.find_pk(db, id)
    recipes = recipe.Recipe.find_category(db, cat)
    categories = category.Category.find_all(db)
    return dict(categories=categories, category=cat, recipes=recipes)

# Manage: Category
@app.get('/manage/categories', template='manage_categories')
@app.post('/manage/categories', template='manage_categories')
def manage_categories(db):
    """ Category managing page. """
    manager = category_manager.CategoryManager(db)
    categories = manager.action()
    hints = manager.hints
    return dict(categories=categories, hints=hints)

# Manage: Recipe
@app.get('/manage/recipe', template='manage_recipe')
@app.get('/manage/recipe/<id:int>', template='manage_recipe')
@app.post('/manage/recipe', template='manage_recipe')
@app.post('/manage/recipe/<id:int>', template='manage_recipe')
def manage_recipe(db, id=None):
    """ Recipe managing page. """
    categories = category.Category.find_all(db)
    manager = recipe_manager.RecipeManager(db)
    rec = manager.action(id)
    hints = manager.hints
    tags = tag.Tag.find_all(db)
    return dict(categories=categories, recipe=rec, hints=hints, tags=tags)

# Manage: Tag
@app.get('/manage/tags', template='manage_tags')
@app.post('/manage/tags', template='manage_tags')
def manage_tag(db):
    """ Tag managing page. """
    categories = category.Category.find_all(db)
    manager = tag_manager.TagManager(db)
    tags = manager.action()
    hints = manager.hints
    return dict(categories=categories, tags=tags, hints=hints)

# Recipe
@app.get('/recipe/<id:int>-<:re:.+>', template='view_recipe')
def view_recipe(db, id):
    """ Recipe view page. """
    rec = recipe.Recipe.find_pk(db, id)
    categories = category.Category.find_all(db)
    return dict(categories=categories, recipe=rec)

# Search
@app.get('/search', template='search')
@app.post('/search', template='search')
def search(db):
    """ Search page. """
    query = bottle.request.forms.getunicode('search-text') or ''
    recipes = []
    if query:
        indexer = indexer_class.Indexer(INDEX_PATH)
        searcher = searcher_class.Searcher(indexer)
        recipes = searcher.search(db, query)
    categories = category.Category.find_all(db)
    return dict(categories=categories, recipes=recipes, query=query)

# Statics ######################################################################
@app.get('/<file:re:(favicon|apple-touch-icon)\.(png|ico)>')
@app.get('/<type:re:(css|img|js)>/<file>')
@app.get('/<type:re:img/upload>/<file>')
def statics(file, type='img'):
    """ Static content like css, images and javascript. """
    return bottle.static_file(file, root='static/'+type)

# Run ##########################################################################
app.run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)