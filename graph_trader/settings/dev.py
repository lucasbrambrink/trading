# Development environment settings

from .default import *

DEBUG = True

INSTALLED_APPS = DEFAULT_APPS + (
    # 'project_core',
    'backtest',
    'home',
    'algo_builder',
    'rest_framework',
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + ()