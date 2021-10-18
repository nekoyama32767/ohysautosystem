import json

from urllib.request import urlopen
import requests

def getwebdata(url,query="",code="utf-8-sig"):
    if query!="":
        url=url+"?"+query
    return requests.get(url).content.decode(code)

def getwebjson(url,query="",code="utf-8-sig"):
    return json.loads(getwebdata(url,query,code))
