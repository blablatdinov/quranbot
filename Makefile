start:
	poetry run python manage.py start

run:
	poetry run python manage.py runserver

lint:
	poetry run isort .
	poetry run flakeheaven lint .

yaspeller:
	poetry run python scripts/lint.py --speller

test:
	poetry run pytest -n 4

cov:
	poetry run pytest --cov=. --cov-report xml:cov.xml -n 4
