ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')
COMMAND = docker exec -it django-app bash -c
MANAGE = python manage.py
DOCKER_FILE = docker-compose -f ./Docker/${ENV}/docker-compose.yml
DOCKER_FILE_TEXT = docker-compose -f ./Docker/<ENV>/docker-compose.yml
EQUALS = is equivalent to
SETTINGS_FLAG = --settings=App.settings.django.${SETTINGS}_settings
TEST_SETTINGS = SETTINGS=test
SETTINGS_FLAG_TEXT = --settings=App.settings.django.<SETTINGS>_settings

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
ifeq (${COVER}, yes)
	${COMMAND} "pytest ${APP} -s --reuse-db --ds=App.settings.django.test_settings --cov --cov-config=.coveragerc -W ignore::django.utils.deprecation.RemovedInDjango41Warning"
else
	${COMMAND} "pytest ${APP} -s --reuse-db --ds=App.settings.django.test_settings -W ignore::django.utils.deprecation.RemovedInDjango41Warning"
endif

test-migrate:
	${TEST_SETTINGS} make migrate

test-populate:
	${TEST_SETTINGS} make populate

test-flush:
	${TEST_SETTINGS} make flush

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
	${COMMAND} "oitnb . --exclude /migrations/* --icons --line-length=79"

check-format:
	${COMMAND} "oitnb --check . --exclude /migrations/* --icons --line-length=79"

sort-imports:
	${COMMAND} "isort **/*.py --lai=2 --sl"

check-imports-order:
	${COMMAND} "isort **/*.py --lai=2 --sl --check"

help:
	@echo ""
	@echo "USAGE: make [command]"
	@echo "You can pass APP, ENV or SETTINGS variable to command likae that:"
	@echo "ENV=Local make up"
	@echo "Note that <ENV> must be capitalized and that <SETTINGS> will be <ENV> in lowercase"
	@echo ""
	@echo "---------------------------------------------------------------------------------"
	@echo "Commands:"
	@echo ""
	@echo " • up: Start the containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} up >"
	@echo ""
	@echo " • upd: Start the containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} up -d >"
	@echo ""
	@echo " • stop: Stop the containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} stop >"
	@echo ""
	@echo " • ps: Show the running containers"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} ps >"
	@echo ""
	@echo " • bash: Open a bash shell in the app container"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE_TEXT} exec app /bin/bash >"
	@echo ""
	@echo " • shell: Open a Django shell_plus in the app container"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} shell_plus ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • startapp: Create a new app"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} startapp <APP>' >"
	@echo ""
	@echo " • createsuperuser: Create a superuser"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} createsuperuser' >"
	@echo ""
	@echo " • migrate: Run migrations"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} makemigrations ${SETTINGS_FLAG_TEXT}' >"
	@echo "                      < ${COMMAND} '${MANAGE} migrate ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • populate: Populate the database"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} populate_db ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • flush: Flush the database"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} flush ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • recreate: Recreated the database"
	@echo "   ↳ ${EQUALS} < make flush >"
	@echo "                      < make migrate >"
	@echo "                      < make populate >"
	@echo ""
	@echo " • create-test-db: Create a test database"
	@echo "   ↳ ${EQUALS} < ${COMMAND} '${MANAGE} create_test_db' >"
	@echo ""
	@echo " • test: Run tests"
	@echo "   ↳ ${EQUALS} < make create-test-db >"
	@echo "                      < ${COMMAND} '${MANAGE} test <APP> --keepdb ${SETTINGS_FLAG_TEXT}' >"
	@echo ""
	@echo " • test-migrate: Run migrations for test environment"
	@echo "   ↳ ${EQUALS} < ${TEST_SETTINGS} make migrate >"
	@echo ""
	@echo " • test-populate: Populate the testing database"
	@echo "   ↳ ${EQUALS} < ${TEST_SETTINGS} make populate>"
	@echo ""
	@echo " • test-flush: Flush the database for tests"
	@echo "   ↳ ${EQUALS} < ${TEST_SETTINGS} make flush>"
	@echo ""
	@echo " • test-recreate: Run recreate for tests"
	@echo "   ↳ ${EQUALS} < make test-flush >"
	@echo "                      < make create_test_db >"
	@echo "                      < make test-migrate >"
	@echo "                      < make test-populate >"
	@echo ""
	@echo " • freeze: Freeze the requirements"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'pip freeze'>"
	@echo ""
	@echo " • logs: Show the logs"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE} logs -f>"
	@echo ""
	@echo " • database: Open a mysql shell"
	@echo "   ↳ ${EQUALS} < ${DOCKER_FILE} exec database mysql -u<USER> -p<PASSWORD> >"
	@echo ""
	@echo " • format: Format the code"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'oitnb . --exclude /migrations/* --icons --line-length=79' >"
	@echo ""
	@echo " • check-format: Check the code for formatting"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'oitnb --check . --exclude /migrations/* --icons --line-length=79' >"
	@echo ""
	@echo " • sort-imports: Sort the imports according PEP 8 and PEP 328"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'isort **/*.py --lai=2 --sl' >"
	@echo ""
	@echo " • check-imports-order: Check the order of the imports according PEP 8 and PEP 328"
	@echo "   ↳ ${EQUALS} < ${COMMAND} 'isort **/*.py --lai=2 --sl --check' >"
	@echo ""
	@echo " • help: Show this help"
	@echo ""
	@echo "---------------------------------------------------------------------------------"
