from flask import Flask# 載入 Flask
from flask import request,jsonify
from flask import redirect
from flask import render_template
import json
import pandas as pd
import numpy as np
import datetime
#匯入模型
from lifetimes import GammaGammaFitter
from lifetimes import BetaGeoFitter


app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/",
)



def getRFM():
    # read RFM csv
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSRJAYjbzy0TdmOKPD6Q_ubs9gn1W2iGgSUeyhi81FlBNtyaJvrSIwapi1sxOAb-GCCuvXoElDXzQ70/pub?output=csv')
    # convert Timestamp type to Datetime
    df['Date'] = pd.to_datetime(df['Date'])
    # RFM table
    df['days'] = (datetime.datetime.strptime('2023-12-29', '%Y-%m-%d') - df['Date']).dt.days
    rfm = df.groupby(by=['C_ID']).agg(
        recency=('days', min),
        frequency=('C_ID', 'size'),
        monetary=('SalesAmount', 'mean'),
        senior=('days', max),
        since=('Date', min)
    )
    rfm['log_monetary'] = np.log(rfm['monetary'])
    # print(rfm)
    return rfm

def getCLV():
    rfm = getRFM()
    #我們定義的平均顧客壽命是6個月
    retain = rfm[rfm['frequency']>1] #我們只取出購買頻率>1的(不是短期單次的顧客)
    ggf = GammaGammaFitter(penalizer_coef=0.001)
    ggf.fit(retain['frequency'],retain['monetary'])
    conditional_avg_profit = ggf.conditional_expected_average_profit(rfm['frequency'],rfm['recency'])
    
    bgf = BetaGeoFitter(penalizer_coef=0.1).fit(rfm['frequency'], rfm['recency'], rfm['senior'])

    
    clv = ggf.customer_lifetime_value(
        bgf,
        rfm['frequency'],
        rfm['recency'],
        rfm['senior'],
        rfm['monetary'],
        time=12,
        discount_rate=0.01
    )

    clv_list = clv.tolist()
    table = []

    for i in range(len(clv)):
      table.append([i+1, round(clv_list[i],2)])

    clv_df = pd.DataFrame(table, columns=['Customer Number', 'CLV Value'])

    
    return clv_df


# 建立路徑 / 對應的處理函式
@app.route("/")
def index():
    rfm_data = getRFM()
    clv_data = getCLV()  
    
    return render_template("index.html", rfm_data=rfm_data,clv_data=clv_data)

@app.route("/member1")
def member1():
    return render_template("member1.html")

@app.route("/member2")
def member2():
    return render_template("member2.html")
   

#啟動網站伺服器,可透過port參數指定埠號
app.run(port=8000)