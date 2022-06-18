SHELL := /bin/bash
ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')
DBUSER ?= user
DBPASSWORD ?= password
HOST ?= "127.0.0.1"
COMMAND = docker exec -i django-app bash -c
MANAGE = python manage.py
DOCKER_FILE = docker-compose -f ./Docker/${ENV}/docker-compose.yml
SETTINGS_FLAG = --settings=App.settings.django.${SETTINGS}_settings
TEST_SETTINGS = SETTINGS=test
PYTEST_SETTINGS = --reuse-db --ds=App.settings.django.test_settings -W ignore::django.utils.deprecation.RemovedInDjango41Warning -p no:cacheprovider
COVERAGE_SETTINGS = --cov --cov-config=.coveragerc
COVERAGE_WITH_HTML_SETTINGS = ${COVERAGE_SETTINGS} --cov-report=html

PING_DB = docker exec database mysqladmin --user=user --password=password --host ${HOST} ping

OITNB_SETTINGS = --exclude="/migrations/*" --icons --line-length=79
ISORT_SETTINGS = --known-local-folder=App/ --skip-glob="**/migrations/*" --skip-glob="**/.env/*" --lai=2 --sl --use-parentheses --trailing-comma --force-grid-wrap=0 --multi-line=3

all: ## Main command, just needed to type `make`. Is equivalent to `make up`.
	@make up

help:	## Show this help which show all the possible make targets and its description.
	@sed -ne '/^[a-zA-Z_-]/ s/^/• / ; /@sed/!s/## //p' $(MAKEFILE_LIST)

up: ## Start the containers running the app.
	@${DOCKER_FILE} up

upd: ## Start the containers detached.
	@${DOCKER_FILE} up -d

ps: ## Show the containers status.
	@${DOCKER_FILE} ps

stop: ## Stop the containers.
	@${DOCKER_FILE} stop

bash: ## Open a bash shell in the django container.
	@${DOCKER_FILE} exec app /bin/bash

shell: ## Open the shell_plus of django. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} shell_plus ${SETTINGS_FLAG}"

migrate: ## Creates and applies the django migrations. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} makemigrations ${SETTINGS_FLAG}"
	@${COMMAND} "${MANAGE} migrate ${SETTINGS_FLAG}"

populate: ## Populates the database with dummy data. You can modify the number of instances created with INSTANCES parameter.
ifeq (${INSTANCES},)
	@${COMMAND} "${MANAGE} populate_db -i 50 ${SETTINGS_FLAG}"
else
	@${COMMAND} "${MANAGE} populate_db -i $(INSTANCES) ${SETTINGS_FLAG}"
endif

flush: ## Flush the database. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} flush ${SETTINGS_FLAG}"

show_urls: ## Show the urls of the app. You can modify grep a string with GREP parameter.
ifeq (${GREP},)
	@${COMMAND} "${MANAGE} show_urls"
else
	@${COMMAND} "${MANAGE} show_urls | grep ${GREP}"
endif

recreate: ## Recreate the the database with dummy data.
	@make flush
	@make migrate
	@make populate

create-test-db: ## Create a test database.
	@${COMMAND} "${MANAGE} create_test_db"

test-migrate: ## Creates and applies the django migrations for tests.
	@${TEST_SETTINGS} make migrate

test-populate: ## Populates the database with dummy data for tests.
	@${TEST_SETTINGS} make populate

test-flush: ## Flush the database for tests.
	@${TEST_SETTINGS} make flush

test-recreate: ## Recreate the the database with dummy data for tests.
	@make test-flush
	@make create-test-db
	@make test-migrate
	@make test-populate

test: ## Run the tests. You can modify the app that will be tested with APP parameter.
	@make create-test-db
ifeq (${APP},)
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS}"
else
	@${COMMAND} "pytest ${APP} -s ${PYTEST_SETTINGS}"
endif

cover-test: ## Run the tests with coverage.
	@make create-test-db
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} ${COVERAGE_SETTINGS}"

html-test: ## Run the tests with coverage and html report.
	@make create-test-db
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} ${COVERAGE_WITH_HTML_SETTINGS}"

fast-test: ## Run the tests in parallel
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} -n auto"

database: ## Access the mysql in the database container. You can modify user/password with DBUSER and DBPASSWORD parameters.
	@${DOCKER_FILE} exec database mysql -u${DBUSER} -p${DBPASSWORD}

lint: ## Run the linter
	@${COMMAND} "oitnb . ${OITNB_SETTINGS}"

check-lint: ## Check for linting errors.
	@${COMMAND} "oitnb --check . ${OITNB_SETTINGS}"

check-lint-local: ## Check for linting errors in local, useful for CI.
	@oitnb --check . ${OITNB_SETTINGS}

sort-imports: ## Sort the imports
	@${COMMAND} "isort . ${ISORT_SETTINGS}"

check-imports: ## Check for errors on imports ordering.
	@${COMMAND} "isort . ${ISORT_SETTINGS} --check"

check-imports-local:  ## Check for errors on imports ordering in local, useful for CI.
	@isort . ${ISORT_SETTINGS} --check

wait-db: ## Wait until the database is ready, useful for CI.
	@while [[ @true ]] ; do \
		if ${PING_DB} --silent &> /dev/null; then\
			echo "Database is up!" && break ; \
		fi ; \
		echo "Waiting for the database to be up" && sleep 1 ; \
	done
