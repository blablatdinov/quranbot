import datetime
import os
import re
from typing import List

import boto3
from django.conf import settings
from loguru import logger


class DumpUploader:
    """Класс, выгружающий дамп БД."""

    def __init__(self) -> None:
        self.formatted_date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        if not settings.ENABLE_S3:
            return
        session = boto3.session.Session()
        self.bucket_name = 'blablatdinov'
        self.s3_client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
        )

    def upload_to_storage(self, relative_path: str, upload_to: str = None) -> None:
        """Выгрузка в s3 storage."""
        if not settings.ENABLE_S3:
            return
        if upload_to is None:
            upload_to = f'quranbot_dumps/{relative_path}'
        self.s3_client.upload_file(
            f'{settings.BASE_DIR}/{relative_path}',
            self.bucket_name,
            upload_to,
        )

    def dump_database_for_developers(self) -> None:
        """Выгрузить дамп для разработки.

        Из дампа удаляются сообщения и данные с кнопок.
        """
        command = (
            'pg_dump -U qbot qbot_db -h localhost '
            '--exclude-table-data="bot_init_callbackdata" '
            '--exclude-table-data="bot_init_message" > '
            f'{settings.BASE_DIR}/dumps/dev_dump.sql && gzip {settings.BASE_DIR}/dumps/dev_dump.sql -f'
        )
        os.system(command)

    def remove_file(self, relative_path: str) -> None:
        """Удалить файл."""
        path = os.path.join(settings.BASE_DIR, relative_path)
        os.remove(path)

    def dump_database(self) -> None:
        """Выгрузить дамп."""
        name = f'qbot_db_{self.formatted_date}.sql.gz'
        command = f'pg_dump -U qbot qbot_db -h localhost | gzip -c --best > {settings.BASE_DIR}/{name}'
        os.system(command)
        self.upload_to_storage(name)
        self.remove_file(name)

    def find_unused_logs(self) -> List[str]:
        """Поиск неиспользуемых логов."""
        walker = os.walk(f'{settings.BASE_DIR}/logs')
        files = next(walker)[2]
        result = [
            file for file in files if re.search(r'app\..+log', file)
        ]
        return result

    def remove_unused_logs(self) -> None:
        """Удалить неиспользуемые логи."""
        for file in self.find_unused_logs():
            self.remove_file(f'logs/{file}')

    def dump_logs(self) -> None:
        """Выгрузить логи в s3."""
        logs_archive_filename = f'logs_{self.formatted_date}.tar.gz'
        command = f'tar zcvf {logs_archive_filename} logs'
        os.system(command)
        self.upload_to_storage(logs_archive_filename)
        self.remove_file(logs_archive_filename)
        self.remove_unused_logs()

    def __call__(self) -> None:
        """Функция снимает дамп базы данных и загружает его на облако."""
        logger.info('dump start')
        start_time = datetime.datetime.now()
        self.dump_database()
        self.dump_database_for_developers()
        self.dump_logs()
        logger.info(f'Dump uploaded successful {datetime.datetime.now() - start_time}')
