from .base import *


ALLOWED_HOSTS = [
    '10.0.2.2',
    '10.0.3.2',
    'localhost',
    'vcelnice-api'
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'vcelnice',
    #     'USER': 'vcelar',
    #     'PASSWORD': 'rudna',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'data', 'db.sqlite3'),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += [
    # 'debug_toolbar',
]

INTERNAL_IPS = ('10.0.2.2',)

TO_EMAIL_RECIPIENTS = ['Oleg Yapparov <oyapparov@gmail.com>']
