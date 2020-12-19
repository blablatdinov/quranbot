git pull
/home/www/code/quranbot/venv/bin/python /home/www/code/quranbot/manage.py migrate
sudo supervisorctl restart qbot qbot_worker
