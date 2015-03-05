# Recipe Manager "NomNomNom"

A simple Python and SQLite based recipe manager.

## Other work

- [Bottle by Marcel Hellkamp](http://bottlepy.org)
- [Chosen by Patrick Filler and Matthew Lettini](http://harvesthq.github.io/chosen/)
- [cx_Freeze](http://cx-freeze.sourceforge.net/)
- [Favicons by Aha-Soft](http://www.aha-soft.com/free-icons/free-blue-cloud-icons/)
- [Font "Open Sans" by Steve Matteson](https://profiles.google.com/107777320916704234605/about) ([Source](http://www.google.com/fonts))
- [gridism by @cobyism](http://cobyism.com/gridism/)
- [jQuery by The jQuery Foundation](https://jquery.org/)
- [jQuery-Autocomplete by Tomas Kirda](https://github.com/devbridge/jQuery-Autocomplete)
- [LESS by Alexis Sellier](http://lesscss.org/)
- [normalize.css by Nicolas Gallagher](http://necolas.github.io/normalize.css/)
- [Selenium](http://www.seleniumhq.org/)
- [Whoosh](https://bitbucket.org/mchaput/whoosh/wiki/Home)

## Basic usage

### Tags

You can create any number of tags. Each tag can have any number of synonyms which are connected with each other. This means if you have the tag "coconut milk" with the synonym "cream of coconut" then you can either search for "coconut milk" or "cream of coconut" and it would always have the same results.

### Categories

Each recipe belongs to one ore more categories. Recipes without a category are also allowed. They will show up on the front page. You may use this to "mark" recipes which you want to cook in the near future.

### Recipes

A recipe must have atleast a title. All other fields are not necessary. Any number of images and links is allowed. The first image will show up in recipe lists.

## Tagging and Searching

The integrated Whoosh based search engine finds recipes (by default) by matching the search query against the title, title synonyms and tags (and their synonyms). This means by adding some tags which descripe the main ingredients, type of food... you can easily find everything even in huge recipe collections.

Extended search terms like filtering by category or only showing unrated recipes are also possible. 

Fields in which can be searched are: category, description, info, ingredients, tags, title, titletags (default), rated and rating. For example the term "category:Cocktails rated:no orange" will find all recipes in the category "Cocktails" which are not rated and contain the word "orange" in their title or tags. Explanation of all fields:

- **category:** Searches in the category list of each recipe.
- **description:** Searches in the description of each recipe.
- **info:** Searchs in the info of each recipe.
- **ingredients:** Searchs in the ingredients list of each recipe.
- **tags:** Searchs in the tag list of each recipe.
- **titletags:** Searchs in the title and the tag list of each recipe. This is the default field.
- **rated:** Searchs for recipes which are rated (value "yes") or not rated (value "no").
- **rating:** Searchs for a certain rating value beginning from zero (equivalent to the white star) and up to three (equivalent to three black stars).

Search terms are by default with a logical AND linked. Other possible logical operations are OR and NOT which will exclude a term.

Inexact terms with wildcards using * (any number of letters) and ? (one letter) are also possible.

Whoosh uses an effective system which orders the result list by a match rating. If you want to increase or decrease the importance of a search term you can do this by adding ^ and a number. For example "coffee^2 milk" will search for coffee and milk but doubles the importance of coffee.

## Mobile Support

Mobile browsers are supported. On very small screens the layout will change to a one column design. Also the font size and some margins are increased to allow an easier usage with touch screens. Images are removed from recipe lists to spare the mobile devices from a heavy CPU load.

## Configuration

A default configuration (host, port...) exists but it's also possible to create a user configuration and override existing values. The files are "default.config" (the default configuration) which you shouldn't change and "user.config". If not already existing create the file "user.config" (for example by copying "default.config") and change the values as you wish.

### Values

- ADMIN_USER: *see Users*
- DB_FILE: Name of the SQLite database file.
- DEBUG: If true bottles debugging is activated.
- ENABLE_USERS: *see Users*
- HOME: The home directory.
- HOST: The host address.
- INDEX_PATH:The search index directory.
- LANGUAGE: The default language.
- PORT: The port.
- PW_HASH_ITERATIONS: Number of iterations for password hashes if user support is active.
- RANDOM_RECIPES: Number of random recipes on the index page.
- RENEW_INDEX: If true the search index will be renewed every time the server is restarted.
- STATIC_PATH: Path to static assets like css, javascript and images.
- TRANSLATION_PATH: The translation file directory.

## Export/Import of Recipe

You can export existing recipes while editing them. The exported zip archive contains a json file with description... and all images of the particular recipe. This zip archive can be imported on the new recipe page. This will immediatly create the imported recipe. An exported recipe contains everything except the rating, categories, tags and the author. These values are individual to a particular instance of this recipe manager and are in most cases not shareable.

## Users

By default this recipe manager runs as a single user instance. Meaning everybody can access it. Using the configuration it is possible to enable an basic user and login mechanism. Following keys are relevant:

- ADMIN_USER: Defines the name of the admin user.
- ENABLE_USERS: If true user support is active.

First it is necessary to enable user support. Then set the initial admin user. After this the admin can loggin with his name and any password (it is recommended to do this immediatly). The admin user can then create a user for himself (use the same admin name or change it in the config afterwards). After logging in a second time user support is setup. Additional users can be created. The admin user can create, update and delete users while individual users can only update their own settings (currently only choosing a new password). 

If a user is logged in he is set as the initial author of an recipe. Also while recipes are shared by default the author can deactivate this.

## Translation

Translations are created using the Python/Linux gettext module. Plural support is currently not used. If you want to create a new translation use a tool like [Poedit](http://poedit.net/) and send them to me.

## Dependencies

For execution:

- [Bottle](http://bottlepy.org/docs/dev/)
- [SQLite Plugin for Bottle](http://bottlepy.org/docs/dev/plugins/sqlite.html)
- [Whoosh](https://pypi.python.org/pypi/Whoosh/)

Optional if you want to use [CherryPy](http://www.cherrypy.org/) (Multi-threaded) instead of wsgiref (Single-threaded) as an webserver:

- [CherryPy](https://pypi.python.org/pypi/CherryPy)

For compiling:

- [cx_Freeze](http://cx-freeze.sourceforge.net/)

For tests:

- [Selenium](http://www.seleniumhq.org/)