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

```
ngrok http 8000
```

Копируем url, который имеет протокол https, в моем случае было https://7db5d686bee3.ngrok.io
Этот url вставляем в поле HOST в файле .env

```
./.env
    export HOST=https://7db5d686bee3.ngrok.io
```
Создаем суперпользвоателя

```
./manage.py createsuperuser
```

Запускаем сервер

```
./manage.py runserver
```
