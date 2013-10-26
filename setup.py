import sys
from cx_Freeze import setup, Executable

includefiles = ['empty-db.sqlite', 'static/', 'README.md', 'LICENSE', 'views/', 'Start.bat']
includes = ['helper.html_escape', 'helper.url']
excludes = []
packages = []

base = None # Console application.
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(
    name = 'NomNomNom',
    version = '1',
    description = 'A simple Python and SQLite based recipe manager.',
    author = 'tea2code',
    url = 'https://github.com/tea2code/recipe_manager',
    options = {'build_exe': {'includes': includes, 'excludes': excludes, 'packages': packages, 'include_files': includefiles}}, 
    executables = [Executable('recipe_manager.py', base = base)]
)