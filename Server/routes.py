from flask import Flask, render_template, request,session,current_app, redirect, url_for
import os
import time
from io import BufferedReader
from server import request_img_recog
import json
# from src.Server import *

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
host = "pcvm3-11.instageni.illinois.edu"
port = 12345

@app.route('/')
def gotoIndex():
    return render_template("WebPage.html")

@app.route('/upload',methods=['POST'])
def getsth():
    f=request.files.get("image")
    
    name = f.filename
    if name != None:
        path = basedir + "\\result\\"+name
        f.save(path)

    start_time = time.time()
    result = request_img_recog(host, port, path)

    read = dict()
    read["Answer"]=result
    read["RTT"] = round((time.time() - start_time)*1000)

    return read

if __name__=='__main__': 
    app.run(host ="0.0.0.0", debug=True)