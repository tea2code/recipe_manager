# Recipe Manager "NomNomNom"

A simple Python and SQLite based recipe manager.

## Other work

- [Favicons by Aha-Soft](http://www.aha-soft.com/free-icons/free-blue-cloud-icons/)
- [Font "Open Sans" by Steve Matteson](https://profiles.google.com/107777320916704234605/about) ([Source](http://www.google.com/fonts))

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

Fields in which can be searched are: category, description, info, ingredients, tags, title, titletags (default) and rated. For example the term "category:Cocktails rated:no orange" will find all recipes in the category "Cocktails" which are not rated and contain the word "orange" in their title or tags.

Search terms are by default with a logical AND linked. Other possible logical operations are OR and NOT which will exclude a term.

Inexact terms with wildcards using * (any number of letters) and ? (one letter) are also possible.

Whoosh uses an effective system which orders the result list by a match rating. If you wand to increase or decrease the importance of a search term you can do this by adding ^ and a number. For example "coffee^2 milk" will search for coffee and milk but doubles the importance of coffee.

## Mobile Support

Mobile browsers are supported. On very small screens the layout will change to a one column design. Also the font size and some margins are increased to allow an easier usage with touch screens. Images are removed from recipe lists to spare the mobile devices from a heavy CPU load.

## Dependencies

For execution:

- [Bottle](http://bottlepy.org/docs/dev/)
- [SQLite Plugin for Bottle](http://bottlepy.org/docs/dev/plugins/sqlite.html)
- [Whoosh](https://pypi.python.org/pypi/Whoosh/)

For compiling:

- [cx_Freeze](http://cx-freeze.sourceforge.net/)

For tests:

- [Selenium](http://www.seleniumhq.org/)