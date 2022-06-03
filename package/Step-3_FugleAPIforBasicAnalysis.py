# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 16:28:37 2021

@author: Vivian
基本面消息面技術面籌碼面財務報表
"""

import requests
import pandas as pd
import time 
import json
from pandas import json_normalize
#filePath = r'C:\Users\Vivian\Desktop\資訊碩士\資訊碩二上\畢業論文研究\StockPrediction\其他\news crawler\\'

class FugleAPI:
    def __init__(self,
                 symbol_id=2330,
                 card = 'ROE及ROA'
                 ):
        self.symbol_id = str(symbol_id) 
        self.card = card
        self.cardDict = {
            #基本面
            'ROE及ROA':[130],
            '利潤比率':[52,66,53],
            '營收':[6],
            'EPS':[26],
            '股利政策':[40,97], 
            '成長能力':[47,48,49,6,26],
            '經營能力':[56,58,60,61], #57,59
            '償債能力':[62,63,64],
            
            '本益比河流圖':[39,26,35],
            
            
            #消息面
            '新聞':[50],
            'PTT批踢踢':[73],
            '重大訊息':[4],
            '搜尋熱度':[81],
            '公開職缺數':[80],
            
            #技術面
            '股價K線':[99],
            
            #籌碼面
            '法人買賣超':[5]
            
            }
        
        # self.test = self.ROE及ROA()#self.tableContentDf(0)  #模組化時因測試程式碼不方便，故設立之
        
               
        

        


        
    '''basic aspect'''
    def tableContentDf(self,code):
        if code < 10:
            code = '00'+str(code)
        elif code < 100:
            code = '0'+str(code)
        else:
            code = str(code)
        url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000{}?symbol_id={}'.format(code,self.symbol_id)
        # print('GET URL: ',url)
        
        payload = "symbol_id=" + self.symbol_id
        res = requests.get(url, data = payload)    #使用Request擷取資料類型為payload的資料
        info = json.loads(res.text)                #用json格式讀取res.text
        df = json_normalize(info['data'])          #normalize就是依照json的dictionary結構化，
                                                   #也就是將content中的contentId, contentIdParameter, specName, rawContent個別汲取出來
        # print(df['content.rawContent'])            
        tableContentList = df['content.rawContent']
        tableContentDf = pd.DataFrame(tableContentList[0])
        
        for i in range(1,len(tableContentList)):
            singleContent = pd.DataFrame(tableContentList[i])
            print(singleContent)
            tableContentDf.concat(singleContent)
        return tableContentDf
 
    
    def ROE及ROA(self):#???????????????????????????????到底是我算的對還是它算的對
        #發現它給的資產負債權益淨利都計算正確，但roe,roa卻都錯誤，故自己算
        code = 130
        df = self.tableContentDf(code)
        print(df['equity'][:-1])
        print(df['equity'][1:])
        beginning = df['equity'][1:].reset_index()
        beginning = beginning['equity']
        end = df['equity'][:-1]
        averTotal =  (beginning+end)/2  # 平均股東權益
        df['ROE'] = df['netProfit']/ averTotal  #accNetprofit指的是會計報表上的數字，netprofit指的是本期不累加的profit
        
        beginning = df['asset'][1:].reset_index()
        beginning = beginning['asset']
        end = df['asset'][:-1]
        averTotal =  (beginning+end)/2  # 平均總資產
        df['ROA'] = df['netProfit']/ averTotal
        
        df = df[['year','quarter','ROE','ROA']]
        return df
        #(季)ROE、last4QROE、ROA、last4QROE
        
    def 利潤比率(self):
        code = 52 #毛利率
        df1 = self.tableContentDf(code)
        df1['毛利率'] = df1['value']
        df = df1[['year','quarter','毛利率']]
        
        
        code = 66 #營業利益率
        df2 = self.tableContentDf(code)
        df['營業利益率'] = df2['value']
 
        
        
        code = 53 #稅後淨利率
        df3 = self.tableContentDf(code)
        df['稅後淨利率'] = df3['value']
        
        return df1
        #(季)毛利率、營業利益率、稅後淨利率列表
    
    def 營收(self): 
        code = 6
        df = self.tableContentDf(code)
        # df = json.loads(df['data'])
        data_df = json_normalize(df['data'])
        df1 = df[['year','month']]
        df2 = data_df[['current.revenue', 'current.lastyear', 'current.yoy','current.mom']]
        df2.rename({'current.revenue':'revenue',
                          'current.lastyear':'lastyear',
                          'current.yoy':'YoY',
                          'current.mom':'MoM'},
                          inplace=True, axis='columns')
        df = pd.concat([df1,df2],axis = 1)
        

        return df 
        #(月)營收列表
        
    def EPS(self):
        code = 26
        df1 = self.tableContentDf(code)
        df1['EPS'] = df1['value']
        df = df1[['year','quarter','EPS']]
        return df
    
    def 股利政策(self):
        code = 40
        df = self.tableContentDf(code)  #資訊過於簡化、不採用
        
        code = 97
        df = self.tableContentDf(code)  #年度與特定日期
        return df
        #不一致規格
    
    def 成長能力(self): #QoQ 跟去年同季相比
        code = 47
        df1 = self.tableContentDf(code)
        df1['毛利QoQ'] = df1['yoy']
        df = df1[['year','quarter','毛利QoQ']]
        
        code = 48
        df2 = self.tableContentDf(code)
        df['營業利益QoQ'] = df2['yoy']
        
        
        code = 49
        df3 = self.tableContentDf(code)
        df['稅後淨利QoQ'] = df3['yoy']
        
        code = 6
        df4 = self.營收()
        df4 = df4.groupby(df4.index // 3).sum()
        df4 = ((df4['revenue'] - df4['lastyear']) / df4['lastyear'])[1:-1]
        df4 = df4.reset_index(name='QoQ')
        df['營收QoQ'] = df4['QoQ']
        
        code = 26
        df5 = self.tableContentDf(code)
        df['每股盈餘QoQ']=df5['yoy']
        
        return df
        #(季)毛利QoQ, 營業利益QoQ, 稅後淨利QoQ, 營收QoQ, 每股盈餘QoQ
        
    def 經營能力(self):
        #'經營能力':[56,58,60,61], #57,59
        code = 56
        df1 = self.tableContentDf(code)
        df1['應收款項週轉率'] = df1['value']
        df = df1[['year','quarter','應收款項週轉率']]
        
        code = 58
        df2 = self.tableContentDf(code)
        df['存貨週轉率'] = df2['value']
        
        code = 60
        df3 = self.tableContentDf(code)
        df['不動產及設備週轉率'] = df3['value']
        
        code = 61
        df4 = self.tableContentDf(code)
        df['總資產週轉率'] = df4['value']
        return df
        #(季)
    
    def 償債能力(self):
        # '償債能力':[62,63,64],
        code = 62
        df1 = self.tableContentDf(code)
        df1['流動比率'] = df1['value']
        df = df1[['year','quarter','流動比率']]
        
        code = 63
        df2 = self.tableContentDf(code)
        df['速動比率'] = df2['value']
        
        code = 64
        df3 = self.tableContentDf(code)
        df['利息保障倍數'] = df3['value']
        return df
        #(季)
        
    def 本益比河流圖(self):
        # '本益比河流圖':[39,26,35],
        code = 39
        df1 = self.tableContentDf(code)
        df1['date'] = df1['date'].str[:7]
        df1 = df1.groupby(['date']).max()
        dropRows = len(df1) % 3
        df1 = df1[:-dropRows]
        df1 = df1.reset_index()
        df1 = df1.groupby(df1.index // 3).max()
        df1 = df1[::-1]
        # df1['流動比率'] = df1['value']
        # df = df1[['year','quarter','流動比率']]
        
        code = 26
        df2 = self.tableContentDf(code)
        df2['近4季EPS'] = df2['value']
        df2 = df2['近4季EPS'].iloc[::-1].rolling(4).sum()
        df2 = df2.iloc[::-1]

        print("This function is abandoned because I don't know how to calculate the max, min")
        return df2
        
    def callFunc(self):
        df = 'nothing in df'
        if self.card == 'ROE及ROA':
            df = self.ROE及ROA()
        if self.card == '利潤比率':
            df = self.利潤比率()
        if self.card == '營收':
            df = self.營收()
        if self.card == 'EPS':
            df = self.EPS()
        if self.card == '股利政策':
            df = self.股利政策()
        if self.card == '成長能力':
            df = self.成長能力()
        if self.card == '經營能力':
            df = self.經營能力()
        if self.card == '償債能力':
            df = self.償債能力()
        return df
            
    def quarterAnalysis(self):
        df1 = self.ROE及ROA()
        time.sleep(2)
        df2 = self.利潤比率().iloc[:,2:]
        time.sleep(2)
        df3 = self.EPS().iloc[:,2:]
        time.sleep(2)
        df4 = self.成長能力().iloc[:,2:]
        time.sleep(2)
        df5 = self.經營能力().iloc[:,2:]
        time.sleep(2)
        df6 = self.償債能力().iloc[:,2:]
        time.sleep(2)
        
        df = pd.concat([df1,df2,df3,df4,df5,df6],axis=1)
            
        
        return df

# =============================================================================
# FugleAPI使用方式：兩種不同的呼叫方法
# =============================================================================
#方法1
# df = FugleAPI(card = '利潤比率').callFunc() #為了實現使用迴圈呼叫的目的
#方法2
# df = FugleAPI().quarterAnalysis()            #為了實現方便快速的呼叫欲取得的卡片資訊(FugleAPI().後透過選單選擇內建方法)
# df.to_csv('data/Step-2_QuarterBasicAnalysis.csv', index=False, encoding='big5')

df = FugleAPI().營收()
df.to_csv('data/Step-2_MonthBasicAnalysis.csv', index=False, encoding='big5')


###基本面###
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000026?symbol_id=2330' #EPS，但裡面的QoQ得自己算，並且有accuValue不知道是什麼
#成長能力中的每股盈餘(對應欄位YoY)
#本益比河流圖的每股盈餘
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000130?symbol_id=2330' #ROE及ROA
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000052?symbol_id=2330'  #利潤比率中的毛利率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000066?symbol_id=2330'   #利潤比率中的營業利益率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000053?symbol_id=2330'  #利潤比率中的稅後淨利率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000006?symbol_id=2330' #營收，變成tableContentDf之後還要再處理
                                                                            #成長能力的營收(要自己算出季跟季之間的成長趴數)
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000040?symbol_id=2330' #股利政策中的EPS
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000097?symbol_id=2330' #股利政策中的除了RPS的項目，不重要不管他
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000047?symbol_id=2330'   #成長能力的毛利(對應欄位YoY)
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000048?symbol_id=2330' #成長能力的營業利益(對應欄位YoY)
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000049?symbol_id=2330' #成長能力的稅後淨利(對應欄位YoY)
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000056?symbol_id=2330' #經營能力的應收款項週轉率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000057?symbol_id=2330' #經營能力的我不知道是什麼
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000058?symbol_id=2330' #經營能力的存貨週轉率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000059?symbol_id=2330' #經營能力的我不知道是什麼
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000060?symbol_id=2330' #經營能力的不動產及設備週轉率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000061?symbol_id=2330' #經營能力的總資產週轉率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000062?symbol_id=2330' #償債能力的流動比率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000063?symbol_id=2330' #償債能力的速動比率
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000064?symbol_id=2330' #償債能力的利息保障倍數
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000039?symbol_id=2330' #本益比河流圖的每一天收盤價(季高、季低、季平均從此提出來)
#本淨比河流圖的每一天收盤價，不知道被拿來幹嘛
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000026?symbol_id=2330' #本益比河流圖的每股盈餘(欄位Value近4季相加)
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000035?symbol_id=2330' #本淨比河流圖的每股淨值

###消息面###
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000050?symbol_id=2330' #新聞，但只有最近11筆
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000050?symbol_id=2330&timestamp_start=1546272000000' #新聞，
# #請用timestamp轉換器，這個每天大約有5至10篇新聞，並且這個連新聞內容都包括
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000073?symbol_id=2330&timestamp_start=1640671843999' #PTT批踢踢，所有有台積電的PTT，內容有被剪裁，依樣用時戳查詢
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000004?symbol_id=2330&timestamp_start=1636458540999' #重大訊息
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000081?symbol_id=2330' #搜尋熱度，傳回的值使用range去搜尋就可以看到要的值了
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000080?symbol_id=2330' #公開職缺數，只有近半年

###技術面###
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000099?symbol_id=2330' #股價K線
#股價K線，使用KD線、MACD線、RSI線，這種東西應該要自己算，但是這個很阿莎力地給了近五年每一年的資訊...
#股價K線，這個還要在修改程式取裡面的資料
#趨勢圖，就是每日收盤價^ ^


###籌碼面###
# url = 'https://www.fugle.tw/api/v2/data/contents/FCNT000005?symbol_id=2330' #近3、4年法人買賣超



    
    