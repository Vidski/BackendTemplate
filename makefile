up:
	docker-compose up

stop:
	docker-compose stop

ps:
	docker-compose ps

bash:
	docker-compose exec app /bin/bash

shell:
	docker exec -it django-app bash -c "python manage.py shell_plus ${SETTINGS}"

create-app:
	docker exec -it django-app bash -c "python manage.py create-app ${APP}"

createsuperuser:
	docker exec -it django-app bash -c "python manage.py createsuperuser"

migrate:
	docker exec -it django-app bash -c "python manage.py makemigrations ${SETTINGS}"
	docker exec -it django-app bash -c "python manage.py migrate ${SETTINGS}"

populate:
	docker exec -it django-app bash -c "python manage.py populate_db ${SETTINGS}"

flush:
	docker exec -it django-app bash -c "python manage.py flush ${SETTINGS}"

recreate:
	make flush
	make migrate
	make populate

create-test-db:
	docker exec -it django-app bash -c "python manage.py create_test_db"

test:
	docker exec -it django-app bash -c "python manage.py test ${APP} --keepdb"

test-migrate:
	SETTINGS=--settings=Settings.test_settings make migrate

test-populate:
	SETTINGS=--settings=Settings.test_settings make populate

test-flush:
	SETTINGS=--settings=Settings.test_settings make flush

test-recreate:
	make test-flush
	make create_test_db
	make test-migrate
	make test-populate

freeze:
	# docker exec -it django-app bash -c "pip freeze > requirements.txt"
	docker exec -it django-app bash -c "pip freeze"

logs:
	docker-compose logs -f

database:
	docker-compose exec database mysql -u${USER} -p${PASSWORD}