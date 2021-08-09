from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json';
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']


service = Create_Service(CLIENT_SECRET_FILE , API_NAME , API_VERSION, SCOPES)

#print(dir(service))
def makePublicUrl(file_id):
    file_ids = '1kB5gVHT7CEt_XgMMjfRWjckOkB_oPQn-'
    # file_id = '0B2RgHcy9LUwpb0pobkJUWmRpRC1zSjZOeUh2MnduTjRBSmxV'

    request_body = {
        'role': 'reader',
        'type': 'domain',
        'domain': 'cbsua.edu.ph'
    }

    response_permission = service.permissions().create(
        fileId = file_id,
        body= request_body
    ).execute()

    response_link = service.files().get(
        fileId = file_id,
        fields = 'webViewLink, writersCanShare,copyRequiresWriterPermission , capabilities'
    ).execute()

    print(response_link)



    #service.permission().delete(
    #    fileId = file_id,
    #    permissionId = 'anyoneWithLink'
    #)


