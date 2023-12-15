from flask import Flask# 載入 Flask
from flask import request,jsonify
from flask import redirect
from flask import render_template
import json
import pandas as pd

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/",
)

# 建立路徑 / 對應的處理函式
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member1")
def member1():
    return render_template("member1.html")

@app.route("/member2")
def member2():
    return render_template("member2.html")
   


#啟動網站伺服器,可透過port參數指定埠號
app.run(port=8000)