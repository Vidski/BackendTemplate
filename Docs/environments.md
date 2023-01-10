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
