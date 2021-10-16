run:
	python manage.py runserver

lint:
	bash lint_script.sh

test:
	pytest -n 4

cov:
	pytest --cov=. --cov-report xml:cov.xml -n 4
