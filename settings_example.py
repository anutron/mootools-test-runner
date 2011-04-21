## copy this to settings.py for the default behavior

# Django settings for mootools-test-runner project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'djangomako.middleware.MakoMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'test_runner',
    'depender',
    'django_extensions',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
)

import os
import logging
logging.basicConfig(level=logging.INFO)

DEPENDER_PACKAGE_YMLS = (
#locations of all your package yamls
#in this example, they're all located in the ext directory as submodules
#for example, ext/core/package.yml for core
  os.path.abspath(os.path.join(os.path.dirname(__file__), "ext", "core", "package.yml")),
  os.path.abspath(os.path.join(os.path.dirname(__file__), "ext", "more", "package.yml")),
  os.path.abspath(os.path.join(os.path.dirname(__file__), "ext", "depender", "client", "package.yml")),
)
DEPENDER_SCRIPTS_JSON = []

# Set to true to re-load all JS every time. (slowish)
DEPENDER_DEBUG = True

MOOTOOLS_TEST_LOCATIONS = {
#locations of html tests that should be included in the menu
#these are typically in the Tests directory of the repository
#example: ext/more/Tests

  "more": os.path.abspath(os.path.join(os.path.dirname(__file__), "ext", "more", "Tests"))
}

# You can exclude tests listed in the locations list above by
# adding them to this array. This is useful when you wish to
# reference assets in one test group from another but don't
# want the tests listed in the menu.
EXCLUDED_TESTS = []

MAKO_TEMPLATE_DIRS = (
  os.path.abspath(os.path.join(os.path.dirname(__file__), "test_runner", "templates")),
)

MOOTOOLS_SPECS_AND_BENCHMARKS = ['More-Tests']

MOOTOOLS_RUNNER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "ext", "mootools-runner"))

GENERIC_ASSETS = {
  'Assets.js.test.js': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "Assets.js.test.js")),
  'Assets.css.test.css': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "Assets.css.test.css")),
  'mootools.png': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "mootools.png")),
  'cow.png': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "cow.png")),
  'notExisting.png': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "notExisting.png")),
  'iDontExist.png': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "iDontExist.png")),
  'iDontExistEither.png': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "iDontExistEither.png")),
  'jsonp.js': os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "more", "Specs", "assets", "jsonp.js")),
}

# heighest level directory that markdown files can be read from
DOC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# where to look for doc files
DOCS = {
  "Clientcide": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "clientcide", "Docs")),
  "Behavior": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "behavior", "Docs")),
  "MooTools More": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "more", "Docs")),
}

TITLE_PREFIX = 'MooTools Tests'
