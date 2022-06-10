# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 15:39:42 2022

@author: Vivian
"""
from datetime import datetime, timedelta

import requests
import pandas as pd
import time 
import json

import os


def news_list(symbol_id,url):
    payload = "symbol_id={}".format(symbol_id)
    res = requests.get(url, data = payload)    #使用Request擷取資料類型為payload的資料
    info = json.loads(res.text)                #将已编码的 JSON 字符串解码为 Python 对象
    items = info['data']['content']['rawContent']
    df = pd.json_normalize(items)
    return df


symbol_id = 2330
symbol_id = str(symbol_id)

for year in range(2021,2022):
    year_str = str(year)
    
    for month in range(7,13):
        if month < 10 :
            month_str = '0' + str(month)
        else:
            month_str = str(month)
            
            
            
        if month == 12:
            startDateStr = '{}{}01'.format(year_str,month_str)
            endDateStr = '{}{}05'.format(str(int(year_str)+1), '01' )            
        else:
            startDateStr = '{}{}01'.format(year_str,month_str)
            endDateStr = '{}{}05'.format(year_str, str(int(month_str)+1) )
        date = datetime.strptime(startDateStr,"%Y%m%d")
        endDate = datetime.strptime(endDateStr,"%Y%m%d")
        timestamp = datetime.timestamp(date)
        
        
        count = 0
        while date <= endDate:
            print('Crawling news...',date)
            
            timestamp_url = '{:.0f}'.format(timestamp) +'000'
            url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000050?symbol_id={}&timestamp_start={}'.format(symbol_id,timestamp_url)
            
            
            df = news_list(symbol_id,url)
             
            if count == 0 :
                df_all = df
            else:
                # Remove Duplicate
                allId = df_all['_id']
                idToKeep = ~df._id.isin(allId)
                rowsToKeep = df[idToKeep]
                df_all = pd.concat([df_all, rowsToKeep], ignore_index=True)
                
            lastDate = df_all['timestamp'][len(df_all)-1][:10]
            print(' '*8,'Last news published date was: ',lastDate)
            print(' '*8,'Last news has: ',len(df_all[df_all['timestamp'].str.contains(lastDate)]))

            date = date+timedelta(days=1)
            timestamp = datetime.timestamp(date)
            count += 1
            time.sleep(10)

        df_all.to_csv('data/Step-3_2330HistoryNews/news_{}_{}.csv'.format(symbol_id,startDateStr[:6]),encoding='utf_8_sig',index=False)



    


    



    