# -*- coding: utf-8 -*-


marketKeyword = ['台股','大盤','外資','投信','自營商','法人','加權指數','美股','台灣','美國',
                 '景氣',]
TSMCKeyword = ['半導體','電子','晶圓','台積電','奈米']

otherKeyword = ['金融','鋼鐵','三星','中國','大陸','避險','自行買賣',
                '會計師','分析師',]

# TSMCKeyword = ['半導體']
# TSMCKeyword = ['電子']

import os 
import pandas as pd 
from datetime import datetime, timedelta

rootDirect = 'C:/Users/Vivian/Desktop/資訊碩士/資訊碩二上/畢業論文研究/StockPrediction'
os.chdir(rootDirect)
         
stockListPath = 'data/News/'
newsListPath = 'data/News/Step-3_2330HistoryNews/'

stockList = pd.read_csv(stockListPath+'Step-3_StockCodeList.csv')

def SumSentimentScore(categoryKeyword,category):
    for i_year in range(2017,2019):
        for i_month in range(1,13):
            if i_month < 10 :
                i_month = '0' + str(i_month)

            '''準備把當天沒有資料的天數加進去'''
            if i_month == 12:
                startDateStr = '{}-{}-01'.format(i_year,i_month)
                endDateStr = '{}-{}-01'.format(str(int(i_year)+1), '01' )            
            else:
                startDateStr = '{}-{}-01'.format(i_year,i_month)
                endDateStr = '{}-{}-01'.format(i_year, str(int(i_month)+1) )
            date = datetime.strptime(startDateStr,"%Y-%m-%d")
            endDate = datetime.strptime(endDateStr,"%Y-%m-%d")
            timestamp = datetime.timestamp(date)
        
            count = 0
            for i_key in categoryKeyword:
                for i_stock in range(len(stockList['stock_name'])):
                    # print(stockList['stock_name'][i_stock],'----------',i_key)
                    if stockList['stock_name'][i_stock] == i_key:
                        industry = stockList['industry_category'][i_stock]
                        stockid = stockList['stock_id'][i_stock]
                        name = stockList['stock_name'][i_stock]
                        readPath = 'data/Step-4-A_SentenceSliced/{}/{}_{}/'.format(industry,stockid,name)
                        readFile = '{}{}_{}_{}.csv'.format(i_year,i_month,stockid,name)
                        if os.path.exists(readPath+readFile):
                            df = pd.read_csv(readPath+readFile)
                            df = df.groupby(df['PublishDate'].str[:10]).sum()
                            df.reset_index(inplace=True)
                            
                                
                        else:
                            print('file not exists.')
                            
                if count == 0:                            
                    df_all = df
                    count += 1
                else:                       
                    df_all = pd.concat([df_all, df],ignore_index=True)
                  
                    
                  
                    
                  
                    
                  
            df_all = df_all.groupby(df_all['PublishDate']).sum()
            df_all.reset_index(inplace=True)
            
            
            while date <  endDate:
                date_str = date.strftime('%Y-%m-%d')
                if not df_all['PublishDate'].str.contains(date_str).any()  :
                    print(date_str)
                    df_all.loc[-1] = [date_str,0]
                    df_all.reset_index(drop=True,inplace=True)
                    
                    
                date = date + timedelta(days=1)

            df_all = df_all.sort_values(by=['PublishDate'],ascending = True)
            df_all.to_csv('data/Step-3-A_SentimentScore/'+f'{category}_{i_year}{i_month}.csv', index=False)
            
            
                    
                        
SumSentimentScore(marketKeyword,'market')  
SumSentimentScore(TSMCKeyword,'TSMC')  
                

