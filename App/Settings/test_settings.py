from .settings import *

ENVIRONMENT_NAME = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_database',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'database', # <-- docker host name for db
        'PORT': '3306', # <-- docker port for db
    }
}