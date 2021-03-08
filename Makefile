#@-- help command to show usage of make commands --@#
help:
	@echo "----------------------------------------------------------------------------"
	@echo "-                     Available commands                                   -"
	@echo "----------------------------------------------------------------------------"
	@echo "---> make venv             - To create virtual environment"
	@echo "---> make activate         - To activate virtual environment"
	@echo "---> make install          - To install dependencies from requirements.txt"
	@echo "---> make init-db          - To initialize the database"
	@echo "---> make migrate          - To create a migration file for the changes in the models"
	@echo "---> make update-db        - To update the database with the latest migration"
	@echo "---> make downgrade-db     - To undo the latest migration in the database"
	@echo "---> make init-day-signs   - To seed the database with day signs"
	@echo "---> make init-month-signs - To seed the database with month signs"
	@echo "---> make update           - To update the requirements file"
	@echo "---> make test             - To run all tests and show coverage"
	@echo "---> make lint             - To run the flake8 linter"
	@echo "---> make run              - To start the server"
	@echo "---> make init-app         - To run update-db, init-day-signs, and init-month-signs"
	@echo " "
	@echo "----------------------->>>>>>>>>>>>><<<<<<<<<<<<<<--------------------------"
	@echo "-                     Available Docker commands                            -"
	@echo "----------------------------------------------------------------------------"
	@echo "---> make build         - To build the docker image"
	@echo "---> make start         - To start the containers in the background"
	@echo "---> make start_verbose - To start the containers verbosely"
	@echo "---> make stop          - To stop the api containers"
	@echo "---> make clean         - To delete the application image"
	@echo "---> make help          - To show usage commands"
	@echo "----------------------------------------------------------------------------"



venv:
	@ echo '<<<<<<<<<<Creating virtual environment>>>>>>>>>'
	sudo apt install python3-venv
	python3 -m venv venv
	@ echo ''

activate:
	@ echo '<<<<<<<<<<Activating virtual environment>>>>>>>>>'
	source venv/bin/activate
	@ echo ''

install:
	@ echo '<<<<<<<<<<installing requirements>>>>>>>>>'
	pip install --upgrade pip
	@ echo ''
	pip install --upgrade pip setuptools
	pip install -r requirements.txt

init-db:
	@ echo '<<<<<<<<<<Initialize database>>>>>>>>>'
	flask db init
	@ echo ''

migrate:
	@ echo '<<<<<<<<<<creating migrations>>>>>>>>>'
	flask db stamp head
	flask db migrate --message="$(message)"
	@ echo ''

update-db:
	@ echo '<<<<<<<<<<updating database>>>>>>>>>'
	flask db upgrade head
	@ echo ''

downgrade-db:
	@ echo '<<<<<<<<<<undo last migration>>>>>>>>>'
	flask db downgrade
	@ echo ''

init-day-signs:
	@ echo '<<<<<<<<<<initializing day sign>>>>>>>>>'
	python ethsigns.py database init_day_sign
	@ echo ''

init-month-signs:
	@ echo '<<<<<<<<<<initializing month sign>>>>>>>>>'
	python ethsigns.py database init_month_sign
	@ echo ''
init-year-signs:
	@ echo '<<<<<<<<<<initializing year sign>>>>>>>>>'
	python ethsigns.py database init_year_sign
	@ echo ''

update:
	@ echo '<<<<<<<<<<updating requirements>>>>>>>>>'
	pip freeze | grep -v "pkg-resources" > requirements.txt
	@ echo ''

test:
	@ echo '<<<<<<<<<<Run tests>>>>>>>>>'
	pytest --cov-report term-missing --cov=api
	@ echo ''

run:
	@ echo '<<<<<<<<<<starting server>>>>>>>>>'
	python ethsigns.py runserver
	@ echo ''

lint:
	@ echo '<<<<<<<<<<linting>>>>>>>>>'
	flake8 .
	@ echo ''

init-app:  update-db init-day-signs init-month-signs init-year-signs


#@-- command to build the application--@#
build:
	@echo "<<<<<<<<<<Building application image>>>>>>>>>>>>>>"
	docker-compose build

#@-- command to start the container in the background --@#
start:
	@echo "<<<<<<<<<<Start up the api in the background after building>>>>>>>>>>>>>>"
	@echo ""
	docker-compose up -d

#@-- command to start the application --@#
start_verbose:
	@echo "<<<<<<<<<<Start up the api containers after building>>>>>>>>>>>>>>"
	@echo ""
	docker-compose up

#@-- command to stop the application --@#
stop:
	@echo "<<<<<<<<<<Stop running the api containers>>>>>>>>>>>>>>"
	@echo ""
	docker-compose down

#@-- command to remove the images created --@#
clean:
	@echo "<<<<<<<<<< \033[31m  Remove application image>>>>>>>>>>>>>>"
	@echo ""
	bash cleanup.sh

#@-- help should be run by default when no command is specified --@#
default: help
