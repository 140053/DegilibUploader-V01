import shutil
import os


def file_move(fname, src, dst):
    # Source path
    # /samba/protected/fine/app/public/file   distanation
    # /samba/protected/file source
    # source = src + fname
    # destination = dst
    # source = '/samba/protected/scanndir/file/' + fname
    # Destination path
    # destination = '/samba/protected/fine/app/public/file'
    # Move the content of
    # source to destination
    dest = shutil.move(src + fname, dst)
    print("done")


def delfile(fname):
    if os.path.exists(fname):
        os.remove(fname)
    else:
        print("The file does not exist")


def delfile2(pat, fname):
    pathfname = pat + fname
    print(pathfname)
    if os.path.exists(pathfname):
        os.remove(pathfname)
    else:
        print("The file does not exist")


def movesuccessfile(fname, src, dst):
    dest = shutil.move(src + fname, dst + "BARCODE/")
    print("done")


# move file into a new folder name the code
def msfdir(fname, dstdir, srcPath, codedir):
    dstpath = dstdir + codedir + '/'
    if os.path.isdir(dstpath) == True:
        shutil.move(dstdir + fname, dstpath)
        print('+++++++++++++++++ done ' + fname + ' file move ++++++++++++++++++++++')
    else:

        os.mkdir(os.path.join(dstdir, codedir))
        if os.path.isdir(dstpath) == False:
            print('+++++++++++++++++ Unable to Create Dir ++++++++++++++++++++++')
        else:
            shutil.move(srcPath + fname, dstpath)
            print('+++++++++++++++++ done ' + fname + ' file move ++++++++++++++++++++++')

# fname = filename
# Code = Code or collection code
# year = taon
# basedir = application base directory /samba/protected/digilib-orig-pgDev/app/public/file
# scrdir = scan dir for pdf


def FhandlingBoth(fname, Code, year, basedir, srcdir):
    dstpath = Code + '/' + year + '/'
    if os.path.isdir(os.path.join(basedir, dstpath)):
        # move filte to dspath
        shutil.move(srcdir + fname, os.path.join(basedir, dstpath))
        print('File Successfully saved as b64 and static to server')
    else:
        try:
            fullpath = os.path.join(basedir, dstpath)
            os.makedirs(fullpath)
            # move filte to dspath
            shutil.move(srcdir + fname, os.path.join(basedir, dstpath))
            print('File Successfully saved as b64 and static to server')
        except OSError as error:
            print(error)
