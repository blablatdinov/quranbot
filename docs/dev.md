# Разворачивание для разработки

Клонируем репозиторий на локальную машину.

```
git clone  https://github.com/blablatdinov/quranbot
```

Заходим в директорию и создаем виртуальное окружение.
Подставьте актуальную версию питона.

```
cd quranbot
python -m venv venv
source venv/bin/activate
pip install -r req.txt
```

Заполняем файл .env
```
cp env_vars .env
```

```
docker-compose -f ./docker/dev/docker-compose.yml build
docker-compose -f ./docker/dev/docker-compose.yml up -d
```

Поднимется 2 контейнера с БД и брокером для celery

Подключаемся к контейнеру с БД и загружаем дампы

```
docker exec -ti qbot_db bash
psql -U qbot -d qbot_db < some_file.sql
```
