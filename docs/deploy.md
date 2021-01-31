# Документация по разворачиванию на сервере без докера

```
git clone https://github.com/blablatdinov/quranbot
```

```
cd quranbot
```

```
python -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r req.txt
```

```
cp env_vars .env
```

```
sudo -u postgres psql
```

```
create database qbot_db;
create user qbot with password '...';
GRANT ALL ON DATABASE qbot_db TO qbot;
alter user qbot createdb;
```

```
./manage.py runserver
```

```
psql -U qbot -d qbot_db -h localhost < qbot_db.sql
```

```
./manage.py runserver 0.0.0.0:8010
```

```
./manage.py collectstatic
```

```
gunicorn config.wsgi:application -c deploy/gunicorn.conf.py
celery -A config worker -B -l INFO 
```

```
sudo cp deploy/supervisor_qbot.conf /etc/supervisor/conf.d/
sudo cp deploy/supervisor_qbot_worker.conf /etc/supervisor/conf.d/
sudo service supervisor restart
```

```
./manage.py update webhook
```

```
sudo certbot --nginx
```

```
./manage.py test
```
