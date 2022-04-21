import getjson

import re
import time
import os

import downloadworker
import json
import sys

import datetime

import framework

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
    offsetend=len(infotitlestr)-1
    while infotitlestr[offsetend]!=')':
        offsetend-=1
    titlestr=infotitlestr[:offset]
    metainfostr=infotitlestr[offset+1:offsetend]
    offset=len(titlestr)-2
    offsetend=len(titlestr)-1
    #print(titlestr)
    if ((titlestr[offset-2:offset+1])=="END"):
        offset-=4
        offsetend-=4

    if (titlestr[offset].isdigit() or titlestr[offset]=="."):
        while (titlestr[offset].isdigit() or titlestr[offset]=="."):
            offset-=1
        title=titlestr[:offset-2]

        chapter=titlestr[offset+1:offsetend]
    else:
        chapter="Whole volume"
        title=titlestr[:offset+1]
    metalist=metainfostr.split()
    filename=origintitlestr[:-8]
    info={"title":title,"chapter":chapter,"source":metalist[0],"resolution":metalist[1],"vcode":metalist[2],"acode":metalist[3]}

    return info



def dumptofile(jsondata,filename):
    f=open(filename,"w")
    json.dump(jsondata,f,indent=4)
    f.close()

def totitletxt(jsondata,filename):
    list=sorted([[key,val] for key,val in jsondata.items()],key=lambda now:now[1],reverse=True)
    with open(filename,mode="w") as f:
        f.write("\n".join([now[0] for now in list]))

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
    title_list=json.load(open("titles.json",mode="r"))
    framework.run_multi_flask()
    while True:
        print("check from ohys")
        titlelist=gettitlelistfromfile('animelist.txt')
        try:
            jsondata=(getjson.getwebjson(ohysjsonurl,ohysquery+"&p=0"))
        except:
            time.sleep(60)
            continue
        for record in jsondata:
            if not ("[Ohys-Raws]" in record["t"]):
                continue
            info=nameinfo(record["t"])
            info["url"]=ohysbaseurl+record["a"]
            if not (".torrent" in info["url"]):
                continue

            if (info["resolution"]=="1280x720" or info["resolution"]=="1280x20") and info["chapter"]!="Whole volume":
                if title_list.get(info["title"])==None:
                    title_list[info["title"]]=str(datetime.date.today())
                    dumptofile(title_list,"titles.json")
                    totitletxt(title_list,"titles.txt")

                if (info["title"]  in  titlelist)  and (not("." in info["chapter"])):
                    if local_list.get(info["title"])==None:
                        local_list[info["title"]]={info["chapter"]:info}
                        dumptofile(local_list,"local.json")
                        print("main loop working on:",info)
                        torrentworker.appendwork(info)
                    elif local_list[info["title"]].get(info["chapter"])==None:
                        local_list[info["title"]][info["chapter"]]=info
                        dumptofile(local_list,"local.json")
                        print("main loop working on:",info)
                        torrentworker.appendwork(info)

        time.sleep(60)
        #exit()
#torrentworker.join()
