ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')

up:
	docker-compose -f ./Docker/${ENV}/docker-compose.yml up

upd:
	docker-compose -f ./Docker/${ENV}/docker-compose.yml up -d

stop:
	docker-compose -f ./Docker/${ENV}/docker-compose.yml stop

ps:
	docker-compose -f ./Docker/${ENV}/docker-compose.yml ps

bash:
	docker-compose -f ./Docker/${ENV}/docker-compose.yml exec app /bin/bash

shell:
	docker exec -it django-app bash -c "python manage.py shell_plus --settings=Settings.Django.${SETTINGS}_settings"

create-app:
	docker exec -it django-app bash -c "python manage.py create-app ${APP}"

createsuperuser:
	docker exec -it django-app bash -c "python manage.py createsuperuser"

migrate:
	docker exec -it django-app bash -c "python manage.py makemigrations --settings=Settings.Django.${SETTINGS}_settings"
	docker exec -it django-app bash -c "python manage.py migrate --settings=Settings.Django.${SETTINGS}_settings"

populate:
	docker exec -it django-app bash -c "python manage.py populate_db --settings=Settings.Django.${SETTINGS}_settings"

flush:
	docker exec -it django-app bash -c "python manage.py flush --settings=Settings.Django.${SETTINGS}_settings"

recreate:
	make flush
	make migrate
	make populate

create-test-db:
	docker exec -it django-app bash -c "python manage.py create_test_db"

test:
	docker exec -it django-app bash -c "python manage.py test ${APP} --keepdb  --settings=Settings.Django.test_settings"

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
	docker-compose -f ./Docker/${ENV}/docker-compose.yml logs -f

database:
	docker-compose -f ./Docker/${ENV}/docker-compose.yml exec database mysql -u${USER} -p${PASSWORD}

format:
	docker exec -it django-app bash -c "oitnb . --exclude */migrations/* --icons"

check-format:
	docker exec -it django-app bash -c "oitnb --check . --exclude */migrations/* --icons"
