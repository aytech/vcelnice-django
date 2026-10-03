from .base import *


ALLOWED_HOSTS = [".vcelnicerudna.cz", ".pythonanywhere.com"]

# YouTube embeds require an origin-level Referer for player identification.
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Enable in HTTPS connection
# CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = False

TO_EMAIL_RECIPIENTS = [('Jan Šaroch', 'jan.saroch@email.cz')]
BCC_EMAIL_RECIPIENTS = [('Oleg Yapparov', 'oyapparov@gmail.com')]
