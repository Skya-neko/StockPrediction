import pandas as pd
from datetime import datetime, timedelta 


filePath = './data/'
monthFile = 'Step-2_MonthBasicAnalysis.csv'
quarterFile = 'Step-2_QuarterBasicAnalysis.csv'


month = pd.read_csv(filePath+monthFile)[::-1].reset_index(drop=True)
quarter = pd.read_csv(filePath+quarterFile,encoding='big5')[::-1].reset_index(drop=True)
quarter.drop([0,1,2,3], inplace=True)



# In[]   月營收

data={}

i_date = datetime.strptime('2017-01-01','%Y-%m-%d')
endDate = datetime.strptime('2021-12-31','%Y-%m-%d')

dateList = []
indicatorList = []

count = 0
i_last_mon = i_date.strftime('%Y-%m-%d')[5:7]
while i_date <= endDate:
    dateList.append(i_date.strftime('%Y-%m-%d'))
    i_mon = i_date.strftime('%Y-%m-%d')[5:7]
    if i_mon != i_last_mon:
        count += 1
    indicatorList.append(month['revenue'][count])
    
    
    i_last_mon = i_mon
    i_date += timedelta(days=1)


data['date'] = dateList
data['Rev_Mon'] = indicatorList

dataDf = pd.DataFrame(data)
# dataDf.to_csv(filePath+'allIndicator.csv', index=False)
    
    
    
 # In[]  季指標  


allList = []


for year in range(2017,2022):
    for QQ in range(1,5):
        rowIdx  = quarter['year'].isin([year]) & quarter['quarter'].isin([QQ])
        row = quarter[rowIdx].values.tolist()[0]
        if QQ == 1:
            i_date = datetime.strptime(f'{year}-01-01','%Y-%m-%d')
            endDate = datetime.strptime(f'{year}-03-31','%Y-%m-%d')
            while i_date <= endDate:
                row_copy = row.copy()
                row_copy.append(i_date.strftime('%Y-%m-%d'))
                allList.append(row_copy)
                i_date += timedelta(days=1)
        elif QQ == 2:
            i_date = datetime.strptime(f'{year}-04-01','%Y-%m-%d')
            endDate = datetime.strptime(f'{year}-06-30','%Y-%m-%d')
            while i_date <= endDate:
                row_copy = row.copy()
                row_copy.append(i_date.strftime('%Y-%m-%d'))
                allList.append(row_copy)
                i_date += timedelta(days=1)
        elif QQ == 3:
            i_date = datetime.strptime(f'{year}-07-01','%Y-%m-%d')
            endDate = datetime.strptime(f'{year}-09-30','%Y-%m-%d')
            while i_date <= endDate:
                row_copy = row.copy()
                row_copy.append(i_date.strftime('%Y-%m-%d'))
                allList.append(row_copy)
                i_date += timedelta(days=1)
        elif QQ == 4:
            i_date = datetime.strptime(f'{year}-10-01','%Y-%m-%d')
            endDate = datetime.strptime(f'{year}-12-31','%Y-%m-%d')
            while i_date <= endDate:
                row_copy = row.copy()
                row_copy.append(i_date.strftime('%Y-%m-%d'))
                allList.append(row_copy)
                i_date += timedelta(days=1)


columnsList = quarter.columns.tolist()
columnsList.append('date')

df = pd.DataFrame(allList, columns = columnsList)
df['月營收'] = indicatorList
df = df [[
          'date',
          '月營收',
          'EPS',                                                         #EPS
          '毛利率',                                                      #利潤比率: 營業利益率和稅後淨利率呢
          'ROE','ROA',                                                   #ROE及ROA
          '每股盈餘QoQ','毛利QoQ','營業利益QoQ','稅後淨利QoQ',             #成長能力: 營收季成長率缺值
          '應收款項週轉率','存貨週轉率','不動產及設備週轉率','總資產週轉率', #經營能力
          '流動比率','速動比率','利息保障倍數',                            #償債能力
          ]]

# In[]   大統合

scoreDf = pd.read_csv('data/Step-2_SentimentScore.csv')
stockPriceDf = pd.read_csv('data/Step-2_StockPrice.csv')

label_col = ['close']
score_col = ['Score']
stock_col = ['Trading_Volume','Trading_money','open','max','min','close']
indicator_col = [
          '月營收',
          'EPS',                                                         #EPS
          '毛利率',                                                      #利潤比率: 營業利益率和稅後淨利率呢
          'ROE','ROA',                                                   #ROE及ROA
          '每股盈餘QoQ','毛利QoQ','營業利益QoQ','稅後淨利QoQ',             #成長能力: 營收季成長率缺值
          '應收款項週轉率','存貨週轉率','不動產及設備週轉率','總資產週轉率', #經營能力
          '流動比率','速動比率','利息保障倍數',                            #償債能力
          ]
dataset_col = ['date']
dataset_col.extend(label_col)
dataset_col.extend(score_col)
dataset_col.extend(stock_col)
dataset_col.extend(indicator_col)


datasetList = []
for specDate in range(1,980):
    print(stockPriceDf['date'][specDate])
    
    
    i_date = datetime.strptime(stockPriceDf['date'][specDate], '%Y-%m-%d')
    i_date += timedelta(days=-1)
    i_date_str = i_date.strftime('%Y-%m-%d')
    
    rowList = [i_date_str,stockPriceDf['close'][specDate]]
    
    idx = scoreDf['PublishDate'].isin([i_date_str])
    if scoreDf[idx].empty:
        score_i_date = datetime.strptime(stockPriceDf['date'][specDate], '%Y-%m-%d')
        while scoreDf[idx].empty:
            score_i_date += timedelta(days=-1)
            score_i_date_str = score_i_date.strftime('%Y-%m-%d')
            idx = scoreDf['PublishDate'].isin([score_i_date_str])
        rowList.extend(scoreDf[idx][score_col].values.tolist()[0])
            
    else:
        idx = scoreDf['PublishDate'].isin([i_date_str])
        rowList.extend(scoreDf[idx][score_col].values.tolist()[0])
        # print(scoreDf[idx])
        
    idx = stockPriceDf['date'].isin([i_date_str])
    if stockPriceDf[idx].empty:
        stock_i_date = datetime.strptime(stockPriceDf['date'][specDate], '%Y-%m-%d')
        while stockPriceDf[idx].empty:
            stock_i_date += timedelta(days=-1)
            stock_i_date_str = stock_i_date.strftime('%Y-%m-%d')
            idx = stockPriceDf['date'].isin([stock_i_date_str])
        rowList.extend(stockPriceDf[idx][stock_col].values.tolist()[0])
            
    else:
        idx = stockPriceDf['date'].isin([i_date_str])
        rowList.extend(stockPriceDf[idx][stock_col].values.tolist()[0])
        # print(stockPriceDf[idx][stock_col])
    
    idx = df['date'].isin([i_date_str])
    rowList.extend(df[idx][indicator_col].values.tolist()[0])
    # print(df[idx][indicator_col])
    
    datasetList.append(rowList)
    rowList = []

datasetDf = pd.DataFrame(datasetList, columns = dataset_col)
datasetDf.to_csv('data/Step-1_Dataset.csv',encoding='big5',index=False)

# print(datasetDf.iloc[:,datasetDf.columns != 'close'].columns.tolist())