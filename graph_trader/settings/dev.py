# Development environment settings

from .default import *

DEBUG = True

INSTALLED_APPS = DEFAULT_APPS + (
    'project_core',
    'backtest',
    'home',
    'algo_builder',
    'rest_framework',
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + ()

# Rabbitmq Settings
RABBITMQ_HOST = 'localhost'

# Celery Settings
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'