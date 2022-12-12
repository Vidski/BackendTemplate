## Variables used in target commands
SHELL := /bin/bash
ENV ?= Local
SETTINGS ?= $(shell echo $(ENV) | tr '[:upper:]' '[:lower:]')

## Variables to make targets more readable
COMMAND = docker exec -it django-app bash -c
NON_INTERACTIVE_COMMAND = docker exec -i django-app bash -c
MANAGE = python manage.py
DOCKER_ENV_FILE = --env-file ./Envs/${ENV}/docker.variables.env
DOCKER_COMPOSE_FILE = -f ./Envs/${ENV}/docker-compose.yml
DOCKER_FILE = docker-compose ${DOCKER_COMPOSE_FILE} ${DOCKER_ENV_FILE}
SETTINGS_FLAG = --settings=Project.settings.django.${SETTINGS}_settings

## Modules settings
TOML_PATH = ./Project/settings/pyproject.toml
BLACK_SETTINGS = --config="${TOML_PATH}"
ISORT_SETTINGS = --settings-path="${TOML_PATH}"
INSTALL_FORMAT_MODULES = pip3 install -r ./Envs/format_requirements.txt

## Testing settings
DJANGO_TEST_SETTINGS = --ds=Project.settings.django.test_settings
PYTEST_FLAGS =  -p no:cacheprovider -p no:warnings
PYTEST_SETTINGS = ${PYTEST_FLAGS} ${DJANGO_TEST_SETTINGS}
COVERAGE_SETTINGS = --cov --cov-config=.coveragerc
HTML_PATH = --cov-report=html:./Project/.htmlconv
HTML_COVERAGE_SETTINGS = ${COVERAGE_SETTINGS} ${HTML_PATH}

## Style to print targets in a nice format
STYLE = {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}


.PHONY: help
help:	## Show this help which show all the possible make targets and its description.
	@echo ""
	@echo "The following are the make targets you can use in this way 'make <target>':"
	@echo ""
	@awk ' BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / ${STYLE}' $(MAKEFILE_LIST)
	@echo ""
	@echo "You can change the environment with the ENV parameter in every target."
	@echo "* You can modify the settings with SETTINGS parameter."
	@echo "** You can grep a string with GREP parameter."
	@echo "*** You can modify the number of instances created with INSTANCES parameter."
	@echo "**** You can modify the path that will be tested with TEST_PATH parameter."
	@echo ""
	@echo "You can interact with docker-compose using the following schema:"
	@echo "docker-compose ${DOCKER_COMPOSE_FILE} ${DOCKER_ENV_FILE}"

ifeq (docker,$(firstword $(MAKECMDGOALS)))
  ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(ARGS):;@:)
endif
.PHONY: docker
docker: ## Runs docker compose command. Eg: "make docker up FLAGS=-d".
	@${DOCKER_FILE} $(ARGS) ${FLAGS}

.PHONY: bash
bash: ## Open a bash shell in the django container.
	@${DOCKER_FILE} exec app /bin/bash

.PHONY: shell
shell: ## Open the shell_plus of django. *
	${COMMAND} "${MANAGE} shell_plus ${SETTINGS_FLAG}"

.PHONY: show_urls
show_urls: ## Show the urls of the app. **
ifeq (${GREP},)
	@${COMMAND} "${MANAGE} show_urls"
else
	@${COMMAND} "${MANAGE} show_urls | grep ${GREP}"
endif

.PHONY: flush
flush: ## Flush the database. *
	@${COMMAND} "${MANAGE} flush ${SETTINGS_FLAG}"

.PHONY: migrations
migrations: ## Creates and applies the django migrations. *
	@${COMMAND} "${MANAGE} makemigrations ${SETTINGS_FLAG}"
	@${COMMAND} "${MANAGE} migrate ${SETTINGS_FLAG}"

INSTANCES ?= 50
.PHONY: populate
populate: ## Populates the database with dummy data. ***
	@${COMMAND} "${MANAGE} populate_db -i $(INSTANCES) ${SETTINGS_FLAG}"

.PHONY: test
test: ## Run the tests. ****
	@${COMMAND} "${MANAGE} create_test_db"
ifeq (${TEST_PATH},)
	@${COMMAND} "pytest . --reuse-db ${PYTEST_SETTINGS}"
else
	@${COMMAND} "pytest ${TEST_PATH} --reuse-db ${PYTEST_SETTINGS} -s"
endif

.PHONY: fast-test
fast-test: ## Run the tests in parallel. ****
	@${NON_INTERACTIVE_COMMAND} "pytest . ${PYTEST_SETTINGS} -n auto"

.PHONY: test-with-coverage
test-with-coverage: ## Run the tests with coverage.
	@${COMMAND} "${MANAGE} create_test_db"
	@${COMMAND} "pytest . ${PYTEST_SETTINGS} ${COVERAGE_SETTINGS}"

.PHONY: test-with-html
test-with-html: ## Run the tests with coverage and html report.
	@${COMMAND} "${MANAGE} create_test_db"
	@${COMMAND} "pytest . ${PYTEST_SETTINGS} ${HTML_COVERAGE_SETTINGS}"

.PHONY: check-lint
check-lint: ## Check for linting errors.
ifeq (${ENV}, CI)
	@${INSTALL_FORMAT_MODULES} && black . ${BLACK_SETTINGS} --check
else
	@${COMMAND} "isort . ${ISORT_SETTINGS} --check"
endif

.PHONY: check-imports
check-imports: ## Check for errors on imports ordering.
ifeq (${ENV}, CI)
	@${INSTALL_FORMAT_MODULES} && isort . ${ISORT_SETTINGS} --check
else
	@${COMMAND} "isort . ${ISORT_SETTINGS} --check"
endif

.PHONY: format
format: ## Runs the linter and import sorter.
	@${COMMAND} "black . ${BLACK_SETTINGS}"
	@${COMMAND} "isort . ${ISORT_SETTINGS}"
