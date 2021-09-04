# Dockerize a Celery App With Django And RabbitMQ

Docker and docker-compose are highly recommended to run the example.

1. Bring up the docker stack:
```docker-compose up -d```

2. Django admin is available on http://localhost:8000/admin

3. Check logs:
```docker-compose logs -f```

4. Monitor tasks in flower:
[http://localhost:5555](http://localhost:5555)
