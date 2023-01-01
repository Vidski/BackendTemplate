<h1 align="center">
  <b>Backend App Template</b>
</h1>

<h3 align="center">
  <b><i> Django + Docker + MySQL + Celery + RabbitMQ + Flower + Grafana + Prometheus </i></b>
</h3>

* * *
The goal of this project is to enable an easy-to-use template in order to start developing a web application as quickly and conveniently as possible.

The environment we are looking to build is one that uses Django as a python framework for web development with MySQL as a database, DjangoRESTFramework to build it as an API; Celery with RabbitMQ for managing asynchronous tasks, and Flower for monitoring those tasks.

The project will be in Docker containers that will be already set up just to start coding the project, following as much as possible the [twelve factor app principles](https://12factor.net/es/) in order to be ready to add any kind of environment maintaining coherence and traceability.

This project has features such as:
- Authentication (login and sign up) for users using [JWT](https://jwt.io/).
- Social OAuth for Google, Facebook and Twitter.
- Permissions for admin users.
- Password recovery through email.
- Email system.
- Notification (global emails) system.
- Customization of emails according the preferred language of users.
- Blacklist to allow users receive only those type of emails they are interested in.
- Mailbox where suggestions/bugs/others can be sent.
- Amazon web services S3 buckets compatibility.
- CRON jobs using Celery and RabbitMQ.
- Database caching system to have a better performance using Redis.
- Prometheus statistics that can be easily configured with Grafana.
- CI pipelines, ready to implement the CD part.
- Github templates for issues and pull requests.
- Github releases for merges on master based on tags.
- 100% of test coverage.

## Table of Contents

| Name | Description |
| --- | --- |
|  [Requirements](#requirements)   |  Must have in order to run the project.   |
|  [Nice to have](#nicetohave)     | This would help you a lot to work with this template. |
|  [Nice to look at](#nicetolook)     | Documentation of the resources used in the template. |
|  [Before starting](#beforestarting)     | Naming disclaimer that would be better to do before starting. |
|  [Instructions](#instructions)    | Instructions to raise the project and start developing. |
|  [Main urls](#mainurls)     | Main urls you can access after running the project. |
|  [Observations](#observations)     | Observations in order to interact with the codebase. |
|  [Versions used](#versions)    | Versions used in this project. |
|  [Useful tools](#usefulltools)    | Useful tools to understand/improve this project based on your needs. |

<a name="requirements"></a>

## Requirements
  - [Docker.](https://docs.docker.com/get-docker/)
  - [Docker-Compose.](https://docs.docker.com/engine/reference/commandline/compose/)

<a name="nicetohave"></a>

## Nice to have
  - [Python3.](https://www.python.org/downloads/)
  - [Make.](https://www.gnu.org/software/make/)

<a name="nicetolook"></a>

## Nice to take a look to
- [Docker documentation.](https://docs.celeryproject.org/en/stable/index.html#)
- [Django documentation.](https://docs.djangoproject.com/en/4.1/)
- [DjangoREST documentation.](https://www.django-rest-framework.org/)
- [Django Jet documentation.](https://django-jet-reboot.readthedocs.io/)
- [Celery documentation.](https://docs.celeryproject.org/)
- [RabbitMQ documentation.](https://www.rabbitmq.com/)
- [Flower documentation.](https://flower.readthedocs.io/en/latest/)
- [Grafana documentation.](https://grafana.com/docs/)
- [Prometheus documentation.](https://prometheus.io/docs/introduction/overview/)
- [OpenApi (swagger) documentation.](https://swagger.io/specification/)
- [ReDoc documentation.](https://redoc.ly/docs)

<a name="beforestarting"></a>

## Before starting

- Look at the `User` model and think if it fits your needs, because changing it after some work done can be hard.

- Feel free to set your environment variables as you want on `.env` files.

- You can change the container name by changing the main folder name.

- You can change the project name to your actual app name, just take in mind that you will need to change folder names, docker-compose.yml content, Dockerfile content and some Django settings in order for the container work correctly.


<a name="instructions"></a>

## Instructions

1. Go to root content folder.
2. Raise the docker containers running:
    ```make docker up```

4. That's all!

:warning: Disclaimer: if you don't have make installed, you can run:

`docker-compose -f ./Docker/Local/docker-compose.yml --env-file ./Docker/Local/docker.env up`

<a name="mainurls"></a>

## Main urls

After running the project:

- Django admin will be available on: [http://api.localhost/admin](http://api.localhost/admin)
- Django app will be available on: [http://api.localhost/](http://api.localhost/)
- Flower task monitor will be available on: [http://flower.localhost/](http://flower.localhost/)
- Grafana monitor will be available on: [http://grafana.localhost/](http://grafana.localhost/)
- Prometheus dashboard will be available on: [http://prometheus.localhost/](http://prometheus.localhost/)
- Documentation served by Openapi (Swagger) will be available on: [http://api.localhost/docs/swagger](http://api.localhost/docs/swagger)
- You can also check the documentation server by Redoc on: [http://api.localhost/docs/redoc](http://api.localhost/docs/redoc)

<a name="observations"></a>

## Observations

You can run `make` or `make help` in order to see all the possibles commands you have to interact with the project.

As first steps in order to correctly interact with it, you have to run:

1. `make migrations`
2.  `make populate` This will create fake data, including admin user with credentials:
    - email: admin@admin.com
    - password: adminpassword


Grafana Credentials will be
    - user: admin
    - password: admin

You will be able to change them once you are logged in.

<a name="versions"></a>

## Versions used
* * *
Reviewed on 2022/11/14.

* Docker compose schema version:  3.9
* Python image:  3.10.5
* RabbitMQ image: 3.9.21
* MySQL image:  8.0.30
* Redis image:  7.0.3
* Django version:  4.1.2
* DjangoRESTFramework version:  3.12.4
* Celery version:  5.2.3


<a name="usefulltools"></a>

<h1 align="center">
  <b>Useful tools</b>
</h1>

These are useful tools to customize/develop your django project.

| Links | Description |
| --- | --- |
| [Medium](https://medium.com/@alex521e2/create-a-custom-user-model-in-django-4-0-a5fd7386b3e0) or [Linkedin](https://www.linkedin.com/pulse/create-custom-user-model-django-40-alejandro-acho-mart%25C3%25ADnez/?trackingId=lFj6aKZmHN5pIKDnlOTykQ%3D%3D) posts | Tutorial to modify custom django user model.|
| [Postman API endpoints.zip](https://github.com/Alejandroacho/BackendTemplate/files/10007414/Postman.API.endpoints.zip) | Collections of the endpoints ready to use in postman. |
| [Simple social OAuth frontend](https://github.com/Alejandroacho/SocialOAuth) | This is a small frontend project you can use to test the OAuth endpoints. |
