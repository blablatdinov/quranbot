run:
	poetry run python manage.py run

lint:
	poetry run isort .
	poetry run flake8 .
	poetry run mypy manage.py server tests

test:
	poetry run pytest
