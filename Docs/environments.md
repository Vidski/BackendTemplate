# Environments

In order to make easy the way to handle multiple environments, you will find the `Envs/` folder in the root path of the project. There you will find two fulfilled environments (`Local` and `CI`), that you can use as an example in order to make more.

Even so, here we will explain the structure of an environment and how to implement a deployment-ready environment.

## Structure
```
Envs/
├── Local/
│   ├── __init__.py
│   ├── django_settings.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── test_django_settings.py
│   ├── traefik.yml
│   └── variables.env
├── __init__.py
├── default_django_settings.py
├── default_requirements.py
└── format_requirements.html
```

In the root folder you will find:

- `default_django_settings.py` : Here you will find the basic Django settings that are reusable across all the environments.
- `default_requirements.txt`: In this file are described the basics requirements (such as Django for example), that will be used in any kind  of environment.
- `format_requirements.txt`: These are the requirements to format the code. They are separated from the rest in order to make a job in CI pipeline run faster.

Now in the `Envs/Local` folder you will fine the following files:

- `django_settings.py`: Specific django setting for an environment (such as database connection, debug mode, etc.).
- `docker-compose.yml`: Docker compose file where you have to declare the services you need to run.
- `Dockerfile`: What you want to run in during the image building.
- `requirements.txt`: The specific requirements for the environment.
- `test_django_settings.py`: The settings to run the django tests, probably only needed on `Local` and `CI`.
- `traefik.yml`: Here you have to define the static configuration for the reverse proxy.
- `variables.env`: The environment variables used both in Django and in Docker.

## Deployment-ready environment

In order to be able to deploy a project you have to follow this steps:

1. Have this settings in the django environment settings:
  ````
    ALLOWED_HOSTS: list = [
      "YOUR_DOMAIN.com",
    ]
    URL: str = "http://YOUR_DOMAIN.com"
    DEBUG: bool = False
    ENVIRONMENT_NAME: str = "prod"
  ````

2. Set the environment variables, specially the settings file:
  ````
    DJANGO_SETTINGS_MODULE=Envs.Production.django_settings
  ````

3. Have something similar to this in the Traefik static configuration:
  ````
    # API and dashboard configuration
    api:
      # Dashboard
      dashboard: true
      insecure: false

    # Docker configuration backend
    providers:
      docker:
        exposedByDefault: false

    ping: {}

    # Traefik Logging
    log:
      level: DEBUG

    # Entrypoint
    entryPoints:
      web:
        address: ":80"
      websecure:
        address: ":443"

    # Certificates
    certificatesResolvers:
      myCustomResolver:
        acme:
          email: YOUR_EMAIL@YOUR_DOMAIN.com
          storage: acme.json
          dnsChallenge:
            provider: YOU_PROVIDER
            delayBeforeCheck: 0
  ````

4. Have this at the end of your Dockerfile:
  ````
    EXPOSE 8000
    CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
  ````

5. Have this kind of configuration in the docker-compose file:
version: '3.9'
  ````
services:
  traefik:
    container_name: traefik
    image: traefik:v2.3
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik.yml:/etc/traefik/traefik.yml
    environment:
      - "PROVIDER_SETTINGS=YOUR_PROVIDER_TOKEN"
      # See the documentation below:
      # https://doc.traefik.io/traefik/v1.5/configuration/acme/#provider

  app:
    container_name: django-app
    build:
      context: ../../
      dockerfile: ${DOCKERFILE_PATH}
    image: &app app
    restart: always
    env_file: &envfile
      - ../../Envs/Production/variables.env
    ports:
      - 8000:8000
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`SUBDOMAIN.YOUR_DOMAIN.com`)"
      - "traefik.http.routers.api.service=api"
      - "traefik.http.services.api.loadbalancer.server.port=8000"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=myCustomResolver"
  ````

And that would be all. You will be then ready to deploy using docker. You will be able to see a Kubernetes in other documentation file.

⚠️ Warning: Take in mind that your domain has to be pointing to your host, and have a DNS record like this:

![DNS Record configuration](./images/DNS-record-configuration.png "Secret creation")

## Easy life
In order to make this as easy as possible (takin in mind that you may have more than one service, subdomain, middlewares, etc.), the environments are set in order to get data injected through a `variables.env`, just as in the local environment. The structure this file must have in production/staging/dev is the following one:


````
######################################
# PROJECT
######################################
DO_TOKEN = ""
SECRET_KEY = ""
TEST_EMAI = ""
SUGGESTIONS_EMAIL = ""
TRAEFIK_USER = ""
TRAEFIK_PASSWORD = ""
EMAIL_VERIFICATION_TOKEN_SECRET = ""
SERVER_IP = ""
ENV = Production


######################################
# DATABASE
######################################
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""


######################################
# URLS
######################################
FRONTEND_URL = ""
PROJECT_URL = domain.com
BACKEND_URL = subdomainexample.domain.com
TRAEFIK_UR = ""
GRAFANA_URL = ""
PROMETHEUS_URL = ""
RABBIT_URL = ""
FLOWER_URL = ""
VERIFY_URL = ""


######################################
# Django
######################################
DJANGO_SETTINGS_MODULE = Envs.Production.django_settings


######################################
# SMTP
######################################
EMAIL_HOST = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = ""


######################################
# OAUTH
######################################
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
TWITTER_API_KEY = ""
TWITTER_API_SECRET_KEY = ""
TWITTER_API_BEARER_TOKEN = ""
OAUTH_PASSWORD = ""


######################################
# S3
######################################
AWS_STORAGE_IMAGE_BUCKET_NAME = ""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_S3_REGION_NAME = ""
AWS_S3_SIGNATURE_VERSION = ""


######################################
# Rabbit MQ
######################################
RABBITMQ_DEFAULT_USER = ""
RABBITMQ_DEFAULT_PASS = ""


######################################
# Celery
######################################
export CELERY_BROKER = amqp://${RABBITMQ_DEFAULT_USER}:${RABBITMQ_DEFAULT_PASS}@rabbitmq:5672


######################################
# Flower
######################################
FLOWER_BROKER = amqp://${RABBITMQ_DEFAULT_USER}:${RABBITMQ_DEFAULT_PASS}@rabbitmq:5672


######################################
# System
######################################
PYTHONDONTWRITEBYTECODE = 1


######################################
# Images
######################################
FLOWER = zoomeranalytics/flower:0.9.2-4.0.2-2
RABBIT = rabbitmq:3.9.21
GRAFANA = grafana/grafana:9.0.3
PROMETHEUS = prom/prometheus:v2.37.0
TRAEFIK = traefik:v2.3


######################################
# Docker compose environment Variables
######################################
APP_NAME = BackendTemplate


######################################
# Paths
######################################
DATA_FOLDER = ~/.mdbdata/${APP_NAME}
DOCKERFILE_PATH = ./Envs/Production/Dockerfile
CELERY_PATH = Project.settings.celery_worker.app
PROMETHEUS_YML = ../../Project/settings/prometheus.yml


######################################
# Commands
######################################
START_DJANGO = python3 manage.py runserver 0.0.0.0:8000
START_CELERY_WORKER = celery --app=${CELERY_PATH} worker --concurrency=1 --hostname=worker@%h --loglevel=INFO
START_CELERY_BEAT = python3 -m celery --app=${CELERY_PATH} beat -l debug -f /var/log/App-celery-beat.log --pidfile=/tmp/celery-beat.pid

````


## Important

⚠️ Don't forget to run this command in any server environment:

`make manage collectstatic ENV=<your_env>`

It is needed in order to allow Django to serve the static files needed for the admin site.
