cd /home/www/code/quranbot

git pull
git reset --hard origin/master
export DJANGO_SETTINGS_MODULE=config.settings

poetry install
poetry run python manage.py migrate

supervisorctl restart qbot
supervisorctl restart qbot_worker
