<h1 align="center">
  <b>Backend App Template</b>
</h1>

<h3 align="center">
  <b><i> Django + Docker + MySQL + Celery + RabbitMQ + Flower + Grafana + Prometheus </i></b>
</h3>

* * *
The goal of this project is to enable an easy-to-use and implement template in order to start developing a web app as quickly and conveniently as possible.

The environment we are looking to build is one that uses Django as a python framework for web development with MySQL as a database. Also will be setted up the DjangoRESTFramework to build an API if needed; Celery with RabbitMQ for managing asynchronous tasks, and Flower for monitoring those tasks.

All we be in one Docker container that will be already setted up to just start coding the project.

## Table of Contents

| Name | Description |
| --- | --- |
|  [Requirements](#requirements)   |  Must to have in order to run the project.   | 
|  [Nice to have](#nicetohave)     | This would help you a lot to work with this template. |
|  [Nice to look at](#nicetolook)     | Documentation of the resources used in the template. |
|  [Before starting](#beforestarting)     | Naming disclaimer that would be better to do before starting. |
|  [Nice to have](#nicetohave)     | This would help you a lot to work with this template. |
|  [Instructions](#instructions)    | Instructions to raise the project and start developing. |
|  [Main urls](#mainurls)     | Main urls you can access after running the project. |
|  [Observations](#observations)     | Observation in order to interact with the project |
|  [Versions used](#versions)    | Versions used in this project. |
|  [Useful guides](#usefullguides)    | Useful guides to understand/improve this project on youw needs. |

<a name="requirements"/>

## Requirements
  - [Docker.](https://docs.docker.com/get-docker/)
  - [Docker-Compose.](https://docs.docker.com/engine/reference/commandline/compose/)

<a name="nicetohave"/>

## Nice to have
  - [Python3.](https://www.python.org/downloads/)
  - [Make.](https://www.gnu.org/software/make/)

<a name="nicetolook"/>

## Nice to take a look to
- [Docker documentation.](https://docs.celeryproject.org/en/stable/index.html#)
- [Django documentation.](https://docs.djangoproject.com/en/4.1/)
- [DjangoREST documentation.](https://www.django-rest-framework.org/)
- [Django Jazzmin documentation.](https://django-jazzmin.readthedocs.io/)
- [Celery documentation.](https://docs.celeryproject.org/)
- [RabbitMQ documentation.](https://www.rabbitmq.com/)
- [Flower documentation.](https://flower.readthedocs.io/en/latest/)
- [Grafana documentation.](https://grafana.com/docs/)
- [Prometheus documentation.](https://prometheus.io/docs/introduction/overview/)
- [OpenApi (swagger) documentation.](https://swagger.io/specification/)
- [ReDoc documentation.](https://redoc.ly/docs)

<a name="beforestarting"/>

## Before starting

- Look at the `User` model and think if it fits your needs, because changin it after some work done can be hard.

- Feel free to set your environment variables as you want on ```env.env``` file.

- You can change the container name by changing the main folder name.

- You can change project name to your actual app name, just take in mind that you will need to change folders name, docker-compose.yml content, Dockerfile content and some django settings in order to the container work correctly.


<a name="instructions"/>

## Instructions

1. Go to root content folder.
2. Bring up the docker container running:
    ```make docker up```

4. That's all!

:warning: Disclaimer: if you don't have make installed, you can run: 

```docker-compose -f ./Docker/Local/docker-compose.yml --env-file ./Docker/Local/docker.env up```

<a name="mainurls"/>

## Main urls

After running the project:

- Django admin will be available on: [http://localhost:8000/admin](http://localhost:8000/admin)
- Django app will be available on: [http://localhost:8000/](http://localhost:8000/)
- Flower task monitor will be available on: [http://localhost:5555](http://localhost:5555)
- Grafana monitor will be available on: [http://localhost:3000](http://localhost:3000)
- Prometheus dashboard will be available on: [http://localhost:9090](http://localhost:9090)
- Documentation served by Openapi (Swagger) will be available on: [http://localhost:8000/docs/swagger](http://localhost:8000/docs/swagger/)
- You can also check the documentation server by Redoc on: [http://localhost:8000/docs/redoc](http://localhost:8000/docs/redoc/)

<a name="observations"/>

## Observations

You can run ```make``` or ```make help``` in order to see all the posible commands you have to interact with the project.

As first steps in order to correctly interact with it, you have to run:

1. ```make migrations```
2.  ```make populate``` This will create you fake data, including admin user with credentials:
    - email: admin@admin.com
    - password: adminpassword


Grafana Credentials will be user: ```admin``` and password: ```admin```. You will be able to change them once you get logged in.

Notice that Django admin is customizable due the use of [Django-Jazzmin](https://django-jazzmin.readthedocs.io/) that implements [Adminlte](https://adminlte.io/) + [Bootstrap](https://getbootstrap.com/).


<a name="versions"/>

## Versions used
* * *
Versions that will use the project. Take in mind that python sub versions may change because it will depend on the one used on [python dockerhub image.](https://hub.docker.com/_/python), it will be the same with [RabbitMQ](https://hub.docker.com/_/rabbitmq), and [MySQL](https://hub.docker.com/_/mysql). Even so, the python version in docker container (reviewed on 2022/01/04) is ```3.9.7```.

* Docker compose schema version:  3.9
* Python image:  3.10.5
* RabbitMQ image: 3.9.21
* MySQL image:  8.0.30
* Redis image:  7.0.3
* Django version:  4.1.2
* DjangoRESTFramework version:  3.12.4
* Celery version:  5.2.3


<a name="usefullguides"/>

<h1 align="center">
  <b>Useful guides</b>
</h1>

These are useful guides to customize our django apps, modifying the default User model.

### Use custom django user model

You can check the guide in the [medium](https://medium.com/@alex521e2/create-a-custom-user-model-in-django-4-0-a5fd7386b3e0) or [linkedin](https://www.linkedin.com/pulse/create-custom-user-model-django-40-alejandro-acho-mart%25C3%25ADnez/?trackingId=lFj6aKZmHN5pIKDnlOTykQ%3D%3D) post.
