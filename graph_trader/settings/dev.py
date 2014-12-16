# Development environment settings

from .default import *

DEBUG = True

INSTALLED_APPS = DEFAULT_APPS + (
    'rest_framework',
    'project_core',
    'home',
    'algo_builder',
    'backtest',
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + ()

# Rabbitmq Settings
RABBITMQ_HOST = 'localhost'

# Celery Settings
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'