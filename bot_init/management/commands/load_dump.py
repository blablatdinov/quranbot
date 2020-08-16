import psycopg2
import shutil
import io
import os
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
from django.conf import settings

from bot_init.service import upload_database_dump


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        # SCOPES = ['https://www.googleapis.com/auth/drive']
        # SERVICE_ACCOUNT_FILE = settings.BASE_DIR + '/deploy/quranbot-keys.json'
        # credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        # service = build('drive', 'v3', credentials=credentials)
        # folder_id = '1G_NYTKUHkQixdElU1hOCg4PR2c66zJPB'

        # results = service.files().list(
            # pageSize=1, fields="nextPageToken, files(id)"
        # ).execute()
        # items = results.get('files', [0])
        # pprint(items)

        # file_id = items[0].get('id')
        # request = service.files().get_media(fileId=file_id)
        # fh = io.BytesIO()
        # downloader = MediaIoBaseDownload(fh, request)
        # done = False
        # while done is False:
            # status, done = downloader.next_chunk()
            # print("Download %d%%." % int(status.progress() * 100))

        # with open(settings.BASE_DIR + '/deploy/qbot_db.sql.gz', 'wb') as f:
            # shutil.copyfileobj(fh, f)
            # # f.write(fh.read())

        # command = f'gzip -d {settings.BASE_DIR}/deploy/qbot_db.sql.gz'
        # os.system(command)


        db = settings.DATABASES
        pprint(db.get('USER'))
        # # exit()
        # connection = psycopg2.connect(
            # # dbname=db.get('NAME'),
            # dbname='qbot_db',
            # user=db.get('USER'),
            # host='localhost',
            # password=db.get('PASSWORD')
        # )  # TODO загружать from settings
        # cursor = connection.cursor()
        # cursor.execute(
        # """
        # SELECT table_name FROM information_schema.tables
	# WHERE table_schema = 'public' order by table_name;
        # """
        # )
        # results = cursor.fetchall()
        # tables = []
        # for row in results:
            # tables.append(row[0])
        # print(tables)

        # with connection:
            # with connection.cursor() as local_cursor:
                # local_cursor.execute("\n".join([
                    # f'drop table if exists "{table}" cascade;'
                    # for table in tables]))
        # print('tables deleted')

        command = f"psql -h localhost -U {db.get('USER')} qbot_db < {settings.BASE_DIR}/dumps/qbot_db.sql"
        os.system(command)

        # command = f'/var/lib/postgresql/bin/pg_dump -U qbot qbot_db -h localhost | gzip -c --best > {settings.BASE_DIR}/deploy/qbot_db.sql.gz'
        # os.system(command)

        # name = 'qbot_db.sql.gz'
        # file_path = settings.BASE_DIR + '/deploy/qbot_db.sql.gz'
        # file_metadata = {
                # 'name': name,
                # 'parents': [folder_id]
        # }
        # media = MediaFileUpload(file_path, resumable=True)
        # r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        # print('Dump uploaded succesful')
