# Development environment settings

from .default import *

DEBUG = True

INSTALLED_APPS = DEFAULT_APPS + (
    'home',
    'algo_builder',
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + ()