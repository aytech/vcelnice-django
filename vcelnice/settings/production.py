from .base import *


ALLOWED_HOSTS = ['.vcelnicerudna.cz', '.pythonanywhere.com']

# Enable in HTTPS connection
# CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'data', 'db.sqlite3'),
    }
}

DEBUG = False

TO_EMAIL_RECIPIENTS = ['jan.saroch@email.cz', 'jan.saroch@o2.cz']
