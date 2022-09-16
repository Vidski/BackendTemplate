## Variables used in target commands
SHELL := /bin/bash
ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')
DBUSER ?= user
DBPASSWORD ?= password
HOST ?= "127.0.0.1"

## Variables to make targets more readable
COMMAND = docker exec -it django-app bash -c
NON_INTERACTIVE_COMMAND = docker exec -i django-app bash -c
MANAGE = python manage.py
DOCKER_ENV_FILE = --env-file ./Docker/${ENV}/docker.env
DOCKER_COMPOSE_FILE = -f ./Docker/${ENV}/docker-compose.yml
DOCKER_FILE = docker-compose ${DOCKER_COMPOSE_FILE} ${DOCKER_ENV_FILE}
SETTINGS_FLAG = --settings=Project.settings.django.${SETTINGS}_settings
TEST_SETTINGS = SETTINGS=test

## Modules settings
TOML_PATH = ./Project/settings/pyproject.toml
BLACK_SETTINGS = --config="${TOML_PATH}"
ISORT_SETTINGS = --settings-path="${TOML_PATH}"

## Testing settings
DJANGO_TEST_SETTINGS = --ds=Project.settings.django.test_settings
PYTEST_FLAGS = --reuse-db -p no:cacheprovider -p no:warnings
PYTEST_SETTINGS = ${PYTEST_FLAGS} ${DJANGO_TEST_SETTINGS}
COVERAGE_SETTINGS = --cov --cov-config=.coveragerc
HTML_PATH = --cov-report=html:./Project/.htmlconv
HTML_COVERAGE_SETTINGS = ${COVERAGE_SETTINGS} ${HTML_PATH}

## Style to print targets in a nice format
STYLE = {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}


.PHONY: all
all: ## Main command, just needed to type `make`. Is equivalent to `make up`.
	@make up

.PHONY: help
help:	## Show this help which show all the possible make targets and its description.
	@echo ""
	@echo "The following are the make targets you can use in this way 'make <target>': "
	@echo ""
	@awk ' BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / ${STYLE}' $(MAKEFILE_LIST)

.PHONY: up
up: ## Start the containers running the app.
	@${DOCKER_FILE} up

.PHONY: upd
upd: ## Start the containers detached.
	@${DOCKER_FILE} up -d

.PHONY: build
build: ## Build the containers.
	@${DOCKER_FILE} build

.PHONY: ps
ps: ## Show the containers status.
	@${DOCKER_FILE} ps

.PHONY: stop
stop: ## Stop the containers.
	@${DOCKER_FILE} stop

.PHONY: bash
bash: ## Open a bash shell in the django container.
	@${DOCKER_FILE} exec app /bin/bash

.PHONY: shell
shell: ## Open the shell_plus of django. You can modify the environment with SETTINGS parameter.
	${COMMAND} "${MANAGE} shell_plus ${SETTINGS_FLAG}"

.PHONY: migrate
migrate: ## Creates and applies the django migrations. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} makemigrations ${SETTINGS_FLAG}"
	@${COMMAND} "${MANAGE} migrate ${SETTINGS_FLAG}"

.PHONY: populate
populate: ## Populates the database with dummy data. You can modify the number of instances created with INSTANCES parameter.
ifeq (${INSTANCES},)
	@${COMMAND} "${MANAGE} populate_db -i 50 ${SETTINGS_FLAG}"
else
	@${COMMAND} "${MANAGE} populate_db -i $(INSTANCES) ${SETTINGS_FLAG}"
endif

.PHONY: flush
flush: ## Flush the database. You can modify the environment with SETTINGS parameter.
	@${COMMAND} "${MANAGE} flush ${SETTINGS_FLAG}"

.PHONY: show_urls
show_urls: ## Show the urls of the app. You can grep a string with GREP parameter.
ifeq (${GREP},)
	@${COMMAND} "${MANAGE} show_urls"
else
	@${COMMAND} "${MANAGE} show_urls | grep ${GREP}"
endif

.PHONY: recreate
recreate: ## Recreate the the database with dummy data.
	@make flush
	@make migrate
	@make populate

.PHONY: create-test-db
create-test-db: ## Create a test database.
	@${COMMAND} "${MANAGE} create_test_db"

.PHONY: test-migrate
test-migrate: ## Creates and applies the django migrations for tests.
	@${TEST_SETTINGS} make migrate

.PHONY: test-populate
test-populate: ## Populates the database with dummy data for tests.
	@${TEST_SETTINGS} make populate

.PHONY: test-flush
test-flush: ## Flush the database for tests.
	@${TEST_SETTINGS} make flush

.PHONY: test-recreate
test-recreate: ## Recreate the the database with dummy data for tests.
	@make test-flush
	@make create-test-db
	@make test-migrate
	@make test-populate

.PHONY: test
test: ## Run the tests. You can modify the app that will be tested with PATH parameter.
	@make create-test-db
ifeq (${PATH},)
	@${COMMAND} "pytest . ${PYTEST_SETTINGS}"
else
	@${COMMAND} "pytest ${PATH} -s ${PYTEST_SETTINGS}"
endif

.PHONY: non-interactive-test
non-interactive-test: ## Run the tests in non-interactive mode. Usefull for CI.
	@${NON_INTERACTIVE_COMMAND} "${MANAGE} create_test_db"
	@${NON_INTERACTIVE_COMMAND} "pytest . ${PYTEST_SETTINGS} -n auto"

.PHONY: test-coverage
test-coverage: ## Run the tests with coverage.
	@make create-test-db
	@${COMMAND} "pytest . ${PYTEST_SETTINGS} ${COVERAGE_SETTINGS}"

.PHONY: test-coverage-html
test-coverage-html: ## Run the tests with coverage and html report.
	@make create-test-db
	@${COMMAND} "pytest . ${PYTEST_SETTINGS} ${HTML_COVERAGE_SETTINGS}"

.PHONY: fast-test
fast-test: ## Run the tests in parallel
	@${COMMAND} "pytest ${APP} ${PYTEST_SETTINGS} -n auto"

.PHONY: database
database: ## Access the mysql in the database container. You can modify user/password with DBUSER and DBPASSWORD parameters.
	@${DOCKER_FILE} exec database mysql -u${DBUSER} -p${DBPASSWORD}

.PHONY: lint
lint: ## Run the linter
	@${COMMAND} "black . ${BLACK_SETTINGS}"

.PHONY: check-lint
check-lint: ## Check for linting errors.
	@${COMMAND} "black . ${BLACK_SETTINGS} --check"

.PHONY: check-lint-local
check-lint-local: ## Check for linting errors in local, useful for CI.
	@black . ${BLACK_SETTINGS} --check

.PHONY: sort-imports
sort-imports: ## Sort the imports
	@${COMMAND} "isort . ${ISORT_SETTINGS}"

.PHONY: check-imports
check-imports: ## Check for errors on imports ordering.
	@${COMMAND} "isort . ${ISORT_SETTINGS} --check"

.PHONY: check-imports-local
check-imports-local:  ## Check for errors on imports ordering in local, useful for CI.
	@isort . ${ISORT_SETTINGS} --check

.PHONY: format
format: ## Runs the linter and import sorter at once
	@make lint
	@make sort-imports
