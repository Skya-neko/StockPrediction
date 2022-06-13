import pandas as pd
from datetime import datetime, timedelta 


# Input File
monthFile = './data/Step-2_MonthBasicAnalysis.csv'
quarterFile = './data/Step-2_QuarterBasicAnalysis.csv'
scoreFile = './data/Step-2_SentimentScore.csv'
priceFile = './data/Step-2_StockPrice.csv'

# Output File
datasetFile = './data/Step-1_Dataset.csv'

# ========================================================================
# Monthly Indicators
# ========================================================================
dateList = []
MIndList = []

monthDF = pd.read_csv(monthFile)[::-1].reset_index(drop=True)     # reverse

i_date = datetime.strptime('2017-01-01','%Y-%m-%d')               # pointer
endDate = datetime.strptime('2021-12-31','%Y-%m-%d')

# Get all dates, values  in duration
while i_date <= endDate:
    dateList.append(i_date.strftime('%Y-%m-%d'))
    i_year = i_date.strftime('%Y-%m-%d')[:4]
    i_mon = i_date.strftime('%Y-%m-%d')[5:7]
    i_value = monthDF[ (monthDF['year']==int(i_year)) & (monthDF['month']==int(i_mon)) ]['revenue']
    i_value = i_value.item()                                       # Return the first element in the series
    MIndList.append(i_value)

    i_date += timedelta(days=1)

# Debug data
# data={}
# data['date'] = dateList
# data['Rev_Mon'] = MIndList
# dataDf = pd.DataFrame(data)




# ========================================================================
# Quarterly Indicators
# ========================================================================
QIndList = []

quarterDF = pd.read_csv(quarterFile,encoding='big5')[::-1].reset_index(drop=True)
quarterDF.drop([0,1,2,3], inplace=True)

# Get all dates, values  in duration
for i_year in range(2017,2022):
    for i_quarter in range(1,5):
        mask = ((quarterDF['year'] == i_year) & (quarterDF['quarter'] == i_quarter))
        row = quarterDF[mask].values.tolist()[0]
        if i_quarter == 1:
            i_date = datetime.strptime(f'{i_year}-01-01','%Y-%m-%d')
            endDate = datetime.strptime(f'{i_year}-03-31','%Y-%m-%d')
        elif i_quarter == 2:
            i_date = datetime.strptime(f'{i_year}-04-01', '%Y-%m-%d')
            endDate = datetime.strptime(f'{i_year}-06-30', '%Y-%m-%d')
        elif i_quarter == 3:
            i_date = datetime.strptime(f'{i_year}-07-01', '%Y-%m-%d')
            endDate = datetime.strptime(f'{i_year}-09-30', '%Y-%m-%d')
        elif i_quarter == 4:
            i_date = datetime.strptime(f'{i_year}-10-01', '%Y-%m-%d')
            endDate = datetime.strptime(f'{i_year}-12-31', '%Y-%m-%d')
        while i_date <= endDate:
            row_copy = row.copy()                          # Must use row_copy
            row_copy.append(i_date.strftime('%Y-%m-%d'))
            QIndList.append(row_copy)
            i_date += timedelta(days=1)




# ========================================================================
# Quarterly & Monthly Indicators
# ========================================================================
columnsList = quarterDF.columns.tolist()
columnsList.append('date')

indicatorsDF = pd.DataFrame(QIndList, columns = columnsList)
indicatorsDF['月營收'] = MIndList
indicatorsDF = indicatorsDF [[
          'date',
          '月營收',
          'EPS',                                                         # EPS
          '毛利率',                                                       # 利潤比率: 營業利益率和稅後淨利率呢
          'ROE', 'ROA',                                                  # ROE及ROA
          '每股盈餘QoQ', '毛利QoQ', '營業利益QoQ', '稅後淨利QoQ',             # 成長能力: 營收季成長率缺值
          '應收款項週轉率', '存貨週轉率', '不動產及設備週轉率', '總資產週轉率',    # 經營能力
          '流動比率', '速動比率', '利息保障倍數',                             # 償債能力
          ]]

# ========================================================================
# Stock Price & Sentiment Score & Indicators
# ========================================================================
scoreDf = pd.read_csv(scoreFile)
stockPriceDf = pd.read_csv(priceFile)

label_col = ['close']
score_col = ['Score']
stock_col = ['Trading_Volume', 'Trading_money', 'open', 'max', 'min', 'close']
indicator_col = [
          '月營收',
          'EPS',                                                         # EPS
          '毛利率',                                                       # 利潤比率: 營業利益率和稅後淨利率呢
          'ROE', 'ROA',                                                  # ROE及ROA
          '每股盈餘QoQ', '毛利QoQ', '營業利益QoQ', '稅後淨利QoQ',             # 成長能力: 營收季成長率缺值
          '應收款項週轉率', '存貨週轉率', '不動產及設備週轉率', '總資產週轉率',    # 經營能力
          '流動比率', '速動比率', '利息保障倍數',                             # 償債能力
          ]

dataset_col = ['date']
dataset_col.extend(label_col)
dataset_col.extend(score_col)
dataset_col.extend(stock_col)
dataset_col.extend(indicator_col)


datasetList = []
for specDate in range(1,980):   # ????????????????why 980????
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

    idx = indicatorsDF['date'].isin([i_date_str])
    rowList.extend(indicatorsDF[idx][indicator_col].values.tolist()[0])
    # print(indicatorsDF[idx][indicator_col])

    datasetList.append(rowList)
    rowList = []

datasetDf = pd.DataFrame(datasetList, columns = dataset_col)
datasetDf.to_csv(datasetFile,encoding='big5',index=False)

# print(datasetDf.iloc[:,datasetDf.columns != 'close'].columns.tolist())