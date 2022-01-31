from App.settings.Django.default_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENVIRONMENT_NAME = 'dev'
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'databasename',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'database', # <-- docker host name for db
        'PORT': '3306', # <-- docker port for db
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'sql_mode': 'STRICT_TRANS_TABLES'
        },
        'TEST': {
            # https://docs.djangoproject.com/en/4.0/topics/testing/overview/#the-test-database
            'NAME': 'test_database'
        }
    }
}

# TOKEN TO VERIFY USER VIA EMAIL
EMAIL_VERIFICATION_TOKEN_SECRET = 'hu712dkej_803h7719)a4n-5!5n0cr((2l'

# SMTP CONFIG
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''
