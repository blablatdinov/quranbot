cd /home/www/code/quranbot

#/home/www/code/quranbot/venv/bin/python /home/www/code/quranbot/manage.py dump

git pull
git reset --hard origin/master
source /home/www/code/quranbot/venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings

/home/www/code/quranbot/venv/bin/pip install -U pip
/home/www/code/quranbot/venv/bin/pip install -r /home/www/code/quranbot/requirements.txt
/home/www/code/quranbot/venv/bin/python /home/www/code/quranbot/manage.py migrate
# /home/www/code/quranbot/venv/bin/pytest

<<<<<<< HEAD
# update admin_frontend

cd admin_frontend
=======
# update admin_fronted

cd admin_fronted
>>>>>>> f5a72ec (init vue admin)
npm install
npm run build

supervisorctl restart qbot
supervisorctl restart qbot_worker
