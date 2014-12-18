# Development environment settings

from .default import *

DEBUG = True

INSTALLED_APPS = DEFAULT_APPS + (
    'django.contrib.sites',
    'rest_framework',
    'account',
    'social.apps.django_app.default',
    'bootstrap3',
    'project_core',
    'home',
    'algo_builder',
    'backtest',
)

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + (
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'account.context_processors.account',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.auth_backends.EmailAuthenticationBackend',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
)


#### Site Settings
SITE_ID = 1
# Setup Email server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'investnotice@gmail.com'
EMAIL_HOST_PASSWORD = 'investnotice123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'admin@djangular-2048.com'


#### Rabbitmq Settings
RABBITMQ_HOST = 'localhost'


#### Celery Settings
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


#### Python-Social-Auth Settings
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

LOGIN_REDIRECT_URL = '/'


#### Django-user-accounts Settings
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_USE_AUTH_AUTHENTICATE = True


try:
    from .local_settings import *
except ImportError:
    import sys, traceback
    sys.stderr.write("Warning: Can't find the file 'local_settings.py' in the directory containing {}. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n".format(__file__))
    sys.stderr.write("\nFor debugging purposes, the exception was:\n\n")
    traceback.print_exc()
