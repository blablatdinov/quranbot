start:
	python manage.py start

run:
	python manage.py runserver

lint:
	poetry run isort . && poetry run flake8 .

yaspeller:
	python scripts/lint.py --speller

test:
	pytest -n 4

cov:
	pytest --cov=. --cov-report xml:cov.xml -n 4
