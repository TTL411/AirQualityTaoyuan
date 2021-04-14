#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = "TL"


import json
import sys
import urllib.request as httplib  # 3.x
import ssl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
#三行可呈現中文
from matplotlib.font_manager import FontProperties # 步驟一
plt.rcParams['font.sans-serif'] = ['SimSun'] # 步驟一（替換sans-serif字型）
plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）

context = ssl._create_unverified_context()


url="https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=1ea37a48-4ba4-4eef-8f04-dfca88294189&rid=9e5756d8-f481-4ab8-881a-416dd04fa07f"
req=httplib.Request(url)
try:
    reponse = httplib.urlopen(req, context=context)
    if reponse.code==200:
        if (sys.version_info > (3, 0)):
            contents = reponse.read();
        else:
            contents = reponse.read()
        data = json.loads(contents)
        print(data)     #確認已抓到檔案

        #確認是否有資料    #待確認
        if(len(data)>=1):
            with open('AirQualityTaoyuan.json','w') as f: #存取
                json.dump(data,f)

except:#  處理網路連線異常
    print("error")

with open('AirQualityTaoyuan.json', 'r') as f:
    data = json.load(f)     #json string 轉 Python

# ItemId,ItemName,ItemEngName,ItemUnit,MonitorDate,Concentration

listItemId = []  #項目編號
listItemName = []  # 項目名稱
listItemEngName = []  # 項目英文名稱
listItemUnit = []  # 項目單位
listMonitorDate = []  # 監測日期
listConcentration = []  # 濃度
listPM25=[]
listNO2=[]
listPM10=[]
listO3=[]
listCO=[]
listSO2=[]

#修掉資料錯誤
x=0
while x<len(data):
    listConcentration.append(data[x]["Concentration"])
    if data[x]["Concentration"]=='x':
        data[x]["Concentration"] = data[x]["Concentration"].replace('x', '0')
    x=x+1

for x in range(int(len(data))):
    # 找出相異資料
    # Itemid:<33/細懸浮微粒><7/二氧化氮><4/懸浮微粒><2/一氧化碳><1/二氧化硫>
    if data[x]["ItemId"] not in listItemId:
        listItemId.append(data[x]["ItemId"])
        listItemName.append(data[x]["ItemName"])
        listItemUnit.append(data[x]["ItemUnit"])
        listItemEngName.append(data[x]["ItemEngName"])
    # 記錄相同資訊和監測時間
    if data[x]["MonitorDate"] not in listMonitorDate:
        listMonitorDate.append(data[x]["MonitorDate"])
    if data[x]["ItemId"] == listItemId[0]:  # 33
        listPM25.append(data[x]["Concentration"])
    elif data[x]["ItemId"] == listItemId[1]:  # 7
        listNO2.append(data[x]["Concentration"])
    elif data[x]["ItemId"] == listItemId[2]:  # 4
        listPM10.append(data[x]["Concentration"])
    elif data[x]["ItemId"] == listItemId[3]:  # 3
        listO3.append(data[x]["Concentration"])
    elif data[x]["ItemId"] == listItemId[4]:  # 2
        listCO.append(data[x]["Concentration"])
    elif data[x]["ItemId"] == listItemId[5]:  # 1
        listSO2.append(data[x]["Concentration"])
print(listItemId)
print(listItemName)
print(listItemUnit)
print(listItemEngName)
print(len(listItemId))
print(listPM25)
print(listNO2)
print(listPM10)
print(listO3)
print(listCO)
print(listSO2)

#資料型別轉換
NewlistPM25=[]
print(len(listPM25))
for x in range(len(listPM25)):
    NewlistPM25.append(int(listPM25[x]))

NewlistNO2=[]
print(len(listNO2))
for x in range(len(listNO2)):
    NewlistNO2.append(float(listNO2[x]))

NewlistPM10=[]
print(len(listPM10))
for x in range(len(listPM10)):
    NewlistPM10.append(int(listPM10[x]))

NewlistO3=[]
print(len(listO3))
for x in range(len(listO3)):
    NewlistO3.append(float(listO3[x]))

NewlistCO=[]
print(len(listCO))
for x in range(len(listCO)):
    NewlistCO.append(float(listCO[x]))
NewlistCO.append(0)
print(len(NewlistCO))

NewlistSO2=[]
print(len(listSO2))
for x in range(len(listSO2)):
    NewlistSO2.append(float(listSO2[x]))
NewlistSO2.append(0)
print(len(NewlistSO2))

#畫圖

plt.xticks(rotation=45)
plt.grid(False)
plt.xticks(rotation=45)

plt.plot(listMonitorDate, NewlistPM25, 'r-', label="PM2.5")
plt.plot(listMonitorDate, NewlistNO2, 'b-', label="NO2")
plt.plot(listMonitorDate, NewlistPM10, 'g-', label="PM10")
plt.plot(listMonitorDate, NewlistO3, 'k-', label="O3")
plt.plot(listMonitorDate, NewlistCO, 'c-', label="CO")
plt.plot(listMonitorDate, NewlistSO2, 'y-', label="SO2")
plt.title('Air Quiality')
plt.legend()
plt.show()

