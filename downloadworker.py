import json

import requests

import threading
import time

import os
from urllib.parse import unquote

from qbittorrent import Client

class DownloadWorker:
    seq=[]

    def __init__(self,addr=None):

        if addr==None:
           # self.qb=Client("http://127.0.0.1:8080/")
           self.addr="http://127.0.0.1:8080/"
        else:
            #self.qb=Client("http://"+addr+"/")
	        self.addr="http://"+addr+"/"

        self.seq=[]
        self.thread=threading.Thread(target=self.run)
        self.lock=threading.Lock()
        self.thread.start()

    def appendwork(self,work):
        self.lock.acquire()
        self.seq.append(work)
        self.lock.release()

    def join(self):
        self.thread.join()

    def run(self):
        while (True):

            time.sleep(0.5)
            workon=None
            self.lock.acquire()

            if (self.seq!=[]):
                workon=self.seq.pop(0)

            self.lock.release()
            if workon!=None:
                print("torrent working on:",workon["title"])
                filename=unquote(os.path.basename(workon["url"]))
                r=requests.get(workon["url"],stream=True)
                while not os.path.isfile("./torrent/"+filename):
                    with open("./torrent/"+filename,'wb') as f:
                        pass
                with open("./torrent/"+filename,'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                    self.qb=Client(self.addr)
                    self.qb.login("admin", "adminadmin")
                    self.qb.download_from_file(open("./torrent/"+filename,"rb"))
            if (not threading.main_thread().is_alive()):
                exit()
