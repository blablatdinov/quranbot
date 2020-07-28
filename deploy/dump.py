from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import io
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = BASE_DIR + '/quranbot-keys.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)
#results = service.files().list(pageSize=10, fields='nextPageToken, files(id, name, mimeType)').execute()
#from pprint import pprint
#pprint(results['files'][0]['id'])
#exit()

def main():
    os.system('/var/lib/postgresql/bin/pg_dump -U qbot qbot_db -h localhost > qbot_db.sql')

    folder_id = '1G_NYTKUHkQixdElU1hOCg4PR2c66zJPB'
    name = 'qbot_db.sql'
    file_path = BASE_DIR + '/qbot_db.sql'
    file_metadata = {
            'name': name,
            'parents': [folder_id]
    }
    print(file_path)
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('Dump uploaded succesful')

if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()
    main()
    print(datetime.now() - start)
