import numpy as np
import pandas as pd
import datetime

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
    print(rfm)
getRFM()