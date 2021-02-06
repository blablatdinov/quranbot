cd /home/www/code/quranbot
git pull
/home/www/code/quranbot/venv/bin/python /home/www/code/quranbot/manage.py migrate
supervisorctl restart qbot qbot_worker
