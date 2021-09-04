# Dockerize a Celery App With Django And RabbitMQ

Docker and docker-compose are highly recommended to run the example.

You can change [app]/[App] to your actual app name.

1. Bring up the docker stack:
```docker-compose up```

2. Django admin is available on http://localhost:8000/admin

3. Check logs:
```docker-compose logs -f```

4. Access container shell to interact with django:
```docker-compose exec app /bin/bash```

5. Access MySQL:
```docker-compose exec database -uadmin -ppassword```
You can change user and password on env.env

4. Monitor tasks in flower:
[http://localhost:5555](http://localhost:5555)

In order to actual interact with django admin, you will need to migrate tables and create a super user.
To achieve this, you will need to access the app container shell and run:

```python3 manage.py migrate```

```python3 manage.py createsuperuser```
