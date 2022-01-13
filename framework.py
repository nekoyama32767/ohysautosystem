from flask import Flask,render_template, request, send_from_directory,jsonify,Markup
import json
import random

import threading

lastlength=0


def writetitlestofile(filename,list):
    with open(filename,mode="w") as f:
        f.write("\n".join(list))
        f.write("\n")

def getrawtitlelistfromfile(filename):
    titlelist=[]
    with open(filename,mode='r') as fin:
        while True:
            title=fin.readline()
            if not title:
                break
            titlelist.append(title[:-1])
    return titlelist

def gettitlelistfromfile(filename):
    titlelist=set()
    with open(filename,mode='r') as fin:
        while True:
            title=fin.readline()
            if not title:
                 break
            titlelist.add(title[:-1])
    return titlelist

app=Flask(__name__)

def make_titles_markup(titlelist,reglist):
    markup=""
    for index,now in enumerate(titlelist):
        markup+="<div>\n"
        tid="t_"+str(index)
        check=""
        if now in reglist:
            check="checked"
        markup+=f'<input type="checkbox" id="{tid}" name="{tid}" {check}>\n'
        markup+=f'<label for="{tid}">{now}</label>\n'
        markup+="</div>\n"
    return Markup(markup)


@app.route("/")
def index_page():
    #print("here")
    titlelist=getrawtitlelistfromfile("titles.txt")
    global lastlength
    lastlength=len(titlelist)

    reglist=gettitlelistfromfile("animelist.txt")
    titles=make_titles_markup(titlelist,reglist)
    #titles=Markup('<br>'.join(titlelist))
    return render_template("index.html",titles=titles)

@app.route("/send",methods=['POST'])
def send_check():
    if request.method == "POST":
        titlelist=getrawtitlelistfromfile("titles.txt")
        global lastlength
        if lastlength!=len(titlelist):
            return
        regrawlist=getrawtitlelistfromfile("animelist.txt")
        reglist=gettitlelistfromfile("animelist.txt")

        checklist=set()

        for index,now in enumerate(titlelist):
            tid="t_"+str(index)
            check=request.form.get(tid)
            if not check:
                continue
            checklist.add(now)
            if not (now in reglist):
                regrawlist.insert(0,now)
        for now in reglist:
            if not (now in checklist):
                regrawlist.remove(now)
        writetitlestofile("animelist.txt",regrawlist)
        return render_template("index.html",titles=Markup("<br>".join(regrawlist)))



def run_multi_flask():
    threading.Thread(target=app.run,kwargs={'port':21474,'host':'0.0.0.0'}).start()

if __name__=="__main__":
    run_multi_flask()
    #app.run(host='0.0.0.0',port=21474)
    while True:
        1
