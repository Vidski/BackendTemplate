ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')
COMMAND = docker exec -it django-app bash -c
MANAGE = python manage.py
DOCKER_FILE = docker-compose -f ./Docker/${ENV}/docker-compose.yml
EQUALS = is equivalent to
SETTINGS_FLAG = --settings=Settings.django.${SETTINGS}_settings

up:
	${DOCKER_FILE} up

upd:
	${DOCKER_FILE} up -d

stop:
	${DOCKER_FILE} stop

ps:
	${DOCKER_FILE} ps

bash:
	${DOCKER_FILE} exec app /bin/bash

shell:
	${COMMAND} "${MANAGE} shell_plus ${SETTINGS_FLAG}"

startapp:
	${COMMAND} "${MANAGE} startapp ${APP}"

createsuperuser:
	${COMMAND} "${MANAGE} createsuperuser"

migrate:
	${COMMAND} "${MANAGE} makemigrations ${SETTINGS_FLAG}"
	${COMMAND} "${MANAGE} migrate ${SETTINGS_FLAG}"

populate:
	${COMMAND} "${MANAGE} populate_db ${SETTINGS_FLAG}"

flush:
	${COMMAND} "${MANAGE} flush ${SETTINGS_FLAG}"

recreate:
	make flush
	make migrate
	make populate

create-test-db:
	${COMMAND} "${MANAGE} create_test_db"

test:
	make create-test-db
	${COMMAND} "${MANAGE} test ${APP} --keepdb --settings=Settings.django.test_settings"

test-migrate:
	SETTINGS=--settings=Settings.django.test_settings make migrate

test-populate:
	SETTINGS=--settings=Settings.django.test_settings make populate

test-flush:
	SETTINGS=--settings=Settings.django.test_settings make flush

test-recreate:
	make test-flush
	make create_test_db
	make test-migrate
	make test-populate

freeze:
	${COMMAND} "pip freeze"

logs:
	${DOCKER_FILE} logs -f

database:
	${DOCKER_FILE} exec database mysql -u${USER} -p${PASSWORD}

format:
	${COMMAND} "oitnb . --exclude */migrations/* --icons"

check-format:
	${COMMAND} "oitnb --check . --exclude */migrations/* --icons"
