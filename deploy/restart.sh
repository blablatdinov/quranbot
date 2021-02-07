cd /home/www/code/quranbot
git pull
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.prod
pip install -r /home/www/code/quranbot/requirements.txt
/home/www/code/quranbot/venv/bin/python /home/www/code/quranbot/manage.py migrate
/home/www/code/quranbot/venv/bin/pytest
#supervisorctl restart qbot qbot_worker
