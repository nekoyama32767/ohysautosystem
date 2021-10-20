import getjson

import re
import time
import os

import downloadworker
import json
import sys

def gettitlelistfromfile(filename):
    titlelist=set()
    with open(filename,mode='r') as fin:
        while True:
            title=fin.readline()
            if not title:
                 break
            titlelist.add(title[:-1])
    return titlelist



def nameinfo(origintitlestr):
    infotitlestr=origintitlestr[12:]

    offset=len(infotitlestr)-1
    while infotitlestr[offset]!='(':
        offset-=1

    titlestr=infotitlestr[:offset]
    metainfostr=infotitlestr[offset+1:len(infotitlestr)-13]

    offset=len(titlestr)-2
    offsetend=len(titlestr)-1
    #print(titlestr)
    if ((titlestr[offset-2:offset+1])=="END"):
        offset-=4
        offsetend-=4
    while titlestr[offset].isdigit():
        offset-=1
    title=titlestr[:offset-2]

    chapter=titlestr[offset+1:offsetend]
    metalist=metainfostr.split()

    filename=origintitlestr[:-8]
    info={"title":title,"chapter":chapter,"source":metalist[0],"resolution":metalist[1],"vcode":metalist[2],"acode":metalist[3]}

    return info



def dumptofile(local_list):
    f=open('local.json',"w")
    json.dump(local_list,f,indent=4)
    f.close()

ohysbaseurl="https://ohys.nl/tt/"

ohysjsonurl=ohysbaseurl+"json.php"
ohysquery="dir=disk"

if __name__  == '__main__':
    #print (os.getcwd())
    if len(sys.argv)==1:
        print("local")
        torrentworker=downloadworker.DownloadWorker("127.0.0.1:8018")
    else:
        args=sys.argv
        index=1
        while index<len(args):
            if args[index]=="-b":
                index+=1
                if index<len(args):
                    print(args[index])
                    torrentworker=downloadworker.DownloadWorker(args[index])
                else:
                    print("Wrong usage")
                    exit()
            index+=1

    local_list={}
    with open('local.json',"r") as f:
         local_list= json.load(f)
    #print(local_list)

    while True:
        print("check from ohys")
        titlelist=gettitlelistfromfile('animelist.txt')

        jsondata=(getjson.getwebjson(ohysjsonurl,ohysquery+"&p=0"))
        for record in jsondata:
            info=nameinfo(record["t"])
            info["url"]=ohysbaseurl+record["a"]
            if ((info["title"]  in  titlelist) and (info["resolution"]=="1280x720")):
                if local_list.get(info["title"])==None:
                    local_list[info["title"]]={info["chapter"]:info}
                    dumptofile(local_list)
                    print("main loop working on:",info)
                    torrentworker.appendwork(info)
                elif local_list[info["title"]].get(info["chapter"])==None:
                    local_list[info["title"]][info["chapter"]]=info
                    dumptofile(local_list)
                    print("main loop working on:",info)
                    torrentworker.appendwork(info)

        time.sleep(60)
        #exit()
#torrentworker.join()
