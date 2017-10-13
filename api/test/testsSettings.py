from sofia.settings import *

MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,
    'messages': None,
    'default': None,
    'sessions': None,
    'staticfiles': None,
    'web': None,
    'admin': None,
    'core': None,
    'profiles': None,
    'snippets': None,
    'scaffold_templates': None,
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'api',
]

SECRET_KEY = 'fake-key'
LOGGING = None
