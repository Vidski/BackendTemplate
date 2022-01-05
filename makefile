up:
	docker-compose up

stop:
	docker-compose stop

bash:
	docker-compose exec app /bin/bash

shell:
	docker exec -it django-app bash -c "python manage.py shell_plus ${SETTINGS}"

test:
	docker exec -it django-app bash -c "python manage.py test ${APP}"

freeze:
	# docker exec -it django-app bash -c "pip freeze > requirements.txt"
	docker exec -it django-app bash -c "pip freeze"

logs:
	docker-compose logs -f

database:
	docker-compose exec database mysql -u${USER} -p${PASSWORD}