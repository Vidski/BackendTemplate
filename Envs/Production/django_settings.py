import os
from datetime import timedelta

from Envs.default_django_settings import *


ALLOWED_HOSTS: list = [
    os.environ.get("PROJECT_URL"),
    os.environ.get("BACKEND_URL"),
    os.environ.get("FRONTEND_URL"),
    os.environ.get("SERVER_IP"),
]

CSRF_TRUSTED_ORIGINS: list = [
    f"https://{os.environ.get('PROJECT_URL')}",
    f"https://{os.environ.get('BACKEND_URL')}",
    f"https://{os.environ.get('FRONTEND_URL')}",
    f"https://{os.environ.get('SERVER_IP')}",
    f"http://{os.environ.get('PROJECT_URL')}",
    f"http://{os.environ.get('BACKEND_URL')}",
    f"http://{os.environ.get('FRONTEND_URL')}",
    f"http://{os.environ.get('SERVER_IP')}",
]
URL: str = os.environ.get("BACKEND_URL")
STATIC_ROOT: str = os.path.join(BASE_DIR, "staticfiles")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = False
ENVIRONMENT_NAME: str = os.environ.get("ENV")

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES: dict = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "sql_mode": "STRICT_TRANS_TABLES",
        },
    }
}

# TOKEN TO VERIFY USER VIA EMAIL
EMAIL_VERIFICATION_TOKEN_SECRET: str = os.environ.get(
    "EMAIL_VERIFICATION_TOKEN_SECRET"
)

# Email settings
TEST_EMAIL: str = os.environ.get("TEST_EMAIL")
SUGGESTIONS_EMAIL: str = os.environ.get("SUGGESTIONS_EMAIL")

# Verify email settings
VERIFY_EMAIL_URL: str = f"{os.environ.get('VERIFY_URL')}"

SIMPLE_JWT: dict = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# SMTP CONFIG
EMAIL_HOST: str = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER: str = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD: str = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT: str = os.environ.get("EMAIL_PORT")

## CORS
# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

## SOCIAL OAUTH
# Google
GOOGLE_CLIENT_ID: str = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET: str = os.environ.get("GOOGLE_CLIENT_SECRET")
# Twitter
TWITTER_API_KEY: str = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY: str = os.environ.get("TWITTER_API_SECRET_KEY")
TWITTER_API_BEARER_TOKEN: str = os.environ.get("TWITTER_API_BEARER_TOKEN")
## OAUTH PASSWORD
OAUTH_PASSWORD: str = os.environ.get("OAUTH_PASSWORD")

##AWS S3
AWS_STORAGE_IMAGE_BUCKET_NAME: str = os.environ.get(
    "AWS_STORAGE_IMAGE_BUCKET_NAME"
)
AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME: str = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_SIGNATURE_VERSION: str = os.environ.get("AWS_S3_SIGNATURE_VERSION")
