cd /home/www/code/quranbot

#/home/www/code/quranbot/venv/bin/python /home/www/code/quranbot/manage.py dump

git pull
git reset --hard origin/master
source /home/www/code/quranbot/venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings

/home/www/code/quranbot/venv/bin/pip install -U pip
/home/www/code/quranbot/venv/bin/pip uninstall -y $(/home/www/code/quranbot/venv/bin/pip freeze)
/home/www/code/quranbot/venv/bin/pip install -r /home/www/code/quranbot/requirements.txt
/home/www/code/quranbot/venv/bin/python /home/www/code/quranbot/manage.py migrate
# /home/www/code/quranbot/venv/bin/pytest

supervisorctl restart qbot
supervisorctl restart qbot_worker
