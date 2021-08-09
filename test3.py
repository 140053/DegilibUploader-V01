import  os

try:
    basedir = '/samba/protected/digilib-orig-pgDev/app/public/file/'
    dstpath = 'MSDRM/2018/'
    fullpath = os.path.join(basedir,dstpath)
    print(fullpath)
    os.makedirs(basedir+dstpath)
    # move filte to dspath
    print('File Successfully saved as b64 and static to server')
except OSError as error:
    print(error)

