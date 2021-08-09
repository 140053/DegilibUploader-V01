from googleapiclient.http import MediaFileUpload
from Google import Create_Service
from orig import makePublicUrl

CLIENT_SECRET_FILE = 'credentials.json';
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_metadata = {'name': 'quation.pdf', 'writersCanShare': 'false', 'copyRequiresWriterPermission': 'true',
                 'capabilities.canShare': 'false'}
# media = MediaFileUpload('files/photo.jpg', mimetype='image/jpg')
# media = MediaFileUpload('photo11111111.jpg', mimetype='image/jpg', writersCanShare='false')
media = MediaFileUpload('quation.pdf', mimetype='application/pdf')
file = service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'

).execute()

newfile_id = file.get('id')
print('File ID: %s' % file.get('id'))
makePublicUrl(newfile_id)
