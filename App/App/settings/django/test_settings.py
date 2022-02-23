from App.settings.django.local_settings import *

ENVIRONMENT_NAME = 'test'

STATICFILES_DIRS = ()
STATIC_ROOT = os.path.join(BASE_DIR, 'Static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_database',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'database',  # <-- docker host name for db
        'PORT': '3306',  # <-- docker port for db
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
    }
}
