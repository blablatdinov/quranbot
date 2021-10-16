cd /home/www/code/quranbot

git pull
git reset --hard origin/master
export DJANGO_SETTINGS_MODULE=config.settings

/home/www/.poetry/bin/poetry install --no-dev
/home/www/.poetry/bin/poetry run python manage.py migrate

supervisorctl restart qbot qbot_worker
