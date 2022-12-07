from flask import Flask, render_template, request,session,current_app, redirect, url_for
import os
from io import BufferedReader
from src.client import request_img_recog
import json
# from src.Server import *

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')

def gotoIndex():

    return render_template("WebPage.html")

@app.route('/upload',methods=['GET','POST'])

def getsth():
    print(request.files.get("image"))
    f=request.files.get("image")
    
    name = f.filename
    print(name)
    if name != None:
        path = basedir + "\\result\\"+name
        f.save(path)

    # print(f)
    print("here")

    result = request_img_recog(12345,path)

    
    print("good")
    read = dict()
    read["Answer"]=result
    # read["Answer"]="test"
    read["RTT"] = 1

    return read

if __name__=='__main__': 

    app.run( )