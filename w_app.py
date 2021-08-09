import sys
import os
import platform
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import glob
import time
import mysql.connector
from time import sleep
from connMysql import *
from mfile import *

scrPath = "/samba/protected/digilibUploader/scanSRC/"
dstPath = "/samba/protected/digilib-orig-pgDev/app/public/file/"
dstNorec = "/samba/protected/digilibUploader/scanDST/"

def clearScreen():
    sleep(3)
    #for windows
    if os.name == 'nt':
        _ = os.system('cls')

    if platform.system() == 'Linux':
        _ = os.system('clear') 


def clearScreenASAP():
    #for windows
    if os.name == 'nt':
        _ = os.system('cls')


def on_created(event):
    print( "[" + val + "] Processing.....")
    sleep(4)
    os.chdir(scrPath)
    list_of_files = glob.glob("*.pdf")
    list_of_files.sort(key=os.path.getmtime)
    last_file = list_of_files[len(list_of_files) - 1]
    print(last_file)
    checkrec = checkduplicate(last_file)
    if checkrec == 0:
        b64 = conVB64(last_file)
        # b64 = conBuffer(last_file)
        print(intoFileStorage(b64))
        res = myFunction(last_file)
    else:
        res = []

    if not res:
        if checkrec <= 1:
            print('+++++++++++++++++++++++++++++++++++++*********+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('________________________________________has duplicate______________________________________________')
            print('+++++++++++++++++++++++++++++++++++++*********+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            delfile(last_file)
        else:
            print('+++++++++++++++++++++++++++++++++++++*********+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('________________________________________No Record in system Source_________________________________')
            print('+++++++++++++++++++++++++++++++++++++*********+++++++++++++++++++++++++++++++++++++++++++++++++++++')
            file_move(last_file, scrPath, dstNorec)
        sleep(2)
    else:
        metadata = makeDic(res)
        print("The file " + last_file + " successfully uploaded")
        # movesuccessfile(last_file, scrPath, dstfile)
        # msfdir(last_file,dstfile, dstfile, val)

        if len(metadata["Year"]) == 4:
            in_to_tb(metadata, val, campus, last_file, metadata["Year"] )
            FhandlingBoth(last_file, val, metadata["Year"], dstPath, scrPath)
        else:
            messg = "Confirm Year base on record [" + metadata["Year"] + "]:"
            taonQ = input(messg)
            if taonQ == 'Yes' or taonQ == '':
                in_to_tb(metadata, val, campus, last_file, metadata["Year"])
                FhandlingBoth(last_file, val, metadata["Year"], dstPath, scrPath)
            else:
                # netaon = input("Input the Year for [" + metadata["filename"] + "]:")
                in_to_tb(metadata, val, campus, last_file, taonQ)
                FhandlingBoth(last_file, val, taonQ, dstPath, scrPath)

        # delfile2(dstfile,last_file)
        delfile(last_file)

    # file_move(last_file, scrPath, dstPath)
    clearScreen()


def on_deleted(event):
    print("deleted")
    clearScreen()
    print("[" + campus + "][" + val + "]Monitoring....")


def on_modified(event):
    print("modified")


def on_moved(event):
    print("moved")


val = input("Enter your Course: ")
# campus = input("Enter Your Campus: ")
campus = "Pili"
# dstfile = input("Enter the Destination path: ")
clearScreenASAP()
print('You are uploading for ' + val + ' and Campus of ' + campus)

if __name__ == "__main__":
    event_handler = FileSystemEventHandler()
    # calling functions
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    path = scrPath
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        print("monitoring")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("stop")
    observer.join()
