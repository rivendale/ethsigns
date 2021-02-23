clean:
	@ echo '<<<<<<<<<<cleaning>>>>>>>>>>>'
	find . -type f -name '*.pyc' -delete
	@ echo ''
	find . -type f -name '*.log' -delete

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

init-app:  update-db init-day-signs init-month-signs