run:
	python manage.py runserver

lint:
	python scripts/lint.py

yaspeller:
	python scripts/lint.py --speller

test:
	pytest -n 4

cov:
	pytest --cov=. --cov-report xml:cov.xml -n 4
