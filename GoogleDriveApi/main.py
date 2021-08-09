from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json';
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

Drive = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def Upload_PDF_file(filename):
    file_metadata = {'name': filename, 'writersCanShare': 'false', 'copyRequiresWriterPermission': 'true',
                     'capabilities.canShare': 'false'}
    media = MediaFileUpload('quation.pdf', mimetype='application/pdf')
    file = Drive.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'

    ).execute()
    return file.get('id')


def makeLink(id):
    request_body = {
        'role': 'reader',
        'type': 'domain',
        'domain': 'cbsua.edu.ph'
    }
    response_permission = Drive.permissions().create(
        fileId=id,
        body=request_body
    ).execute()
    response_link = Drive.files().get(
        fileId=id,
        # fields='webViewLink, writersCanShare,copyRequiresWriterPermission , capabilities'
        fields='webViewLink'
    ).execute()
    return response_link


def MainFunc(filename):
    file_id = Upload_PDF_file(filename)
    return makeLink(file_id)


print(MainFunc('quation.pdf'))
