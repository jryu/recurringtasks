from recurringtasks.settings_debug import *
from private_stuff import MY_EMAIL, POSTGRESQL_PASSWORD

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['checklist.jryu.net']


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'checklist',
        'USER': 'checklistuser',
        'PASSWORD': POSTGRESQL_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = 'https://jryu.github.io/recurringtasks/'


SITE_ID = 2


# Email settings
SERVER_EMAIL = 'webmaster@checklist.jryu.net'
MANAGERS = [('Junho Ryu', MY_EMAIL)]
ADMINS = [('Junho Ryu', MY_EMAIL)]


# Security settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
