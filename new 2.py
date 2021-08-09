import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import glob

from tmp.conn import *
from mfile import file_move

def on_created(event):
    os.chdir("D:/python/scanndir/file")
    list_of_files = glob.glob("*.pdf")
    list_of_files.sort(key=os.path.getmtime)
    last_file = list_of_files[len(list_of_files)-1]
    #print(last_file)
    res = myFunction(last_file)
    file_move(last_file)
    metadata = makeDic(res)
    in_to_tb(metadata)
    print(last_file)
    #print("created")


        
def on_deleted(event):
    print("deleted")
        
def on_modified(event):
    print("modified")
        
def on_moved(event):
    print("moved")


if __name__ == "__main__":
    event_handler = FileSystemEventHandler()
    # calling functions
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved


    path = "D:/python/scanndir/file"
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
    