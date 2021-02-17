clean:
	@ echo '<<<<<<<<<<cleaning>>>>>>>>>>>'
	find . -type f -name '*.pyc' -delete
	@ echo ''
	find . -type f -name '*.log' -delete

update-db:
	@ echo '<<<<<<<<<<updating database>>>>>>>>>'
	flask db upgrade head
	@ echo ''

migrate:
	@ echo '<<<<<<<<<<creating migrations>>>>>>>>>'
	flask db stamp head
	@ echo ''
	flask db migrate --message="$(message)"

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

install:
	@ echo '<<<<<<<<<<installing requirements>>>>>>>>>'
	pip install --upgrade pip
	@ echo ''
	pip install --upgrade pip setuptools
	pip install -r requirements.txt

test:
	@ echo '<<<<<<<<<<Run tests>>>>>>>>>'
	pytest --cov-report term-missing --cov=api
	@ echo ''

run:
	@ echo '<<<<<<<<<<starting server>>>>>>>>>'
	python ethsigns.py runserver
	@ echo ''

init-app:  update-db init-day-signs init-month-signs

lint:
	@ echo '<<<<<<<<<<linting>>>>>>>>>'
	flake8 .
	@ echo ''
