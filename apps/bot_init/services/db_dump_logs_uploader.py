import datetime
import os

from loguru import logger
from django.conf import settings
import boto3


class DumpUploader:

    def __init__(self) -> None:
        session = boto3.session.Session()
        self.formatted_date = datetime.datetime.now().strftime('%Y_%m_%d')
        self.bucket_name = "blablatdinov"
        self.s3_client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )

    def upload_to_storage(self, relative_path: str, upload_to: str = None):
        if upload_to is None:
            upload_to = f"quranbot_dumps/{relative_path}"
        self.s3_client.upload_file(
            f"{settings.BASE_DIR}/{relative_path}", 
            self.bucket_name, 
            upload_to,
        )

    def dump_database_for_developers(self):
        command = f"pg_dump -U qbot qbot_db -h localhost --exclude-table-data='bot_init_callbackdata' --exclude-table-data='bot_init_message'> {settings.BASE_DIR}/dumps/dev_dump.sql && gzip {settings.BASE_DIR}/dumps/dev_dump.sql -f"
        os.system(command)

    def remove_file(self, relative_path: str):
        path = os.path.join(settings.BASE_DIR, relative_path)
        os.remove(path)

    def dump_database(self):
        name = f"qbot_db_{self.formatted_date}.sql.gz"
        command = f"pg_dump -U qbot qbot_db -h localhost | gzip -c --best > {settings.BASE_DIR}/{name}"
        os.system(command)
        self.upload_to_storage(name)
        self.remove_file(name)

    def dump_logs(self):
        logs_archive_filename = f"logs_{self.formatted_date}.tar.gz"
        command = f"tar zcvf {logs_archive_filename} logs"
        os.system(command)
        self.upload_to_storage(logs_archive_filename)
        self.remove_file(logs_archive_filename)

    def __call__(self):
        """Функция снимает дамп базы данных и загружет его на облако."""
        logger.info("dump start")
        start_time = datetime.datetime.now()
        self.dump_database()
        self.dump_database_for_developers()
        self.dump_logs()
        logger.info(f"Dump uploaded successful {datetime.datetime.now() - start_time}")
