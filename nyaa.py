
import requests
from bs4 import BeautifulSoup

def get_data():
    url = 'https://nyaa.si/user/ohys'
    res = requests.get(url)
    html_text = res.text
    soup = BeautifulSoup(html_text, "html.parser")
    tbody = soup.find("tbody")
    #print(tbody)
    trs =  tbody.find_all("tr")
    ret = []
    for tr in trs:
        tds = tr.find_all("td")
        td_title = tds[1]
        title = td_title.a.get("title")
        if not ("[Ohys-Raws]" in title):
            continue
        td_torrent = tds[2]
        torrent = td_torrent.find_all("a")[1].get("href")
        #torrent = td_torrent.fina_all("a")
        #print(torrent)
        ret.append({"t":title, "link":torrent})
    return ret
if __name__ == "__main__":
    print(get_data())