"""
Sum the sentiment score of market, TSMC, antiTSMC categories in sentences csv into monthly record csv
(in ./data/Step-3-A_SentimentScore).
"""
import os
import pandas as pd 
from datetime import datetime, timedelta

marketKeyword = ['台股','大盤','外資','投信','自營商','法人','加權指數','美股','台灣','美國','景氣',]
TSMCKeyword = ['半導體','電子','晶圓','台積電','奈米']
antiTSMCKeyword = ['三星', '英特爾']
# otherKeyword = ['金融','鋼鐵','三星','中國','大陸','避險','自行買賣','會計師','分析師',]

stockCodeDF = pd.read_csv('./data/Step-3_StockCodeList.csv')

def sum_sentiment_score ( categoryKeyword, category):
    for i_year in range(2017,2019):
        for i_month in range(1,13):
            # Replace i_month to meet file keywords
            if i_month < 10 :
                i_month = '0' + str(i_month)

            count = 0
            categoryMask = stockCodeDF['stock_name'].isin(categoryKeyword)
            categoryIdxList = categoryMask[categoryMask].index.tolist()
            # Iterate keywords in market, TSMC, antiTSMC list to sum sentiment scores
            for i_key in categoryIdxList:                           
                industry = stockCodeDF['industry_category'][i_key]
                stockid = stockCodeDF['stock_id'][i_key]
                keywords = stockCodeDF['stock_name'][i_key]
                readPath = './data/Step-4-A_SentenceSliced/{}/{}_{}/'.format(industry,stockid,keywords)
                readFile = '{}{}_{}_{}.csv'.format(i_year,i_month,stockid,keywords)
                
                if os.path.exists(readPath+readFile):
                    df = pd.read_csv(readPath+readFile)
                    df = df.groupby(df['PublishDate'].str[:10]).sum()     # Divide by i_date, sum the scores.
                    df.reset_index(inplace=True)

                    if count == 0:  # Check If this is the first df we created, let it be df_all.
                        df_all = df
                        count += 1
                    else:           # Concat new df into df_all
                        df_all = pd.concat([df_all, df], ignore_index=True)
                        
                else:
                    continue        # News file doesn't exist

            # Sum all the Scores in the category keyword list by i_date
            df_all = df_all.groupby(df_all['PublishDate']).sum()     
            df_all.reset_index(inplace=True)

            # To make sure we go through every day in the news sliced file and add score "0" to null date,
            # we iterate from the beginning of this month to the beginning of next month.
            if i_month == 12:
                startDateStr = '{}-{}-01'.format(i_year, i_month)
                endDateStr = '{}-{}-01'.format(str(i_year + 1), '01')
            else:
                startDateStr = '{}-{}-01'.format(i_year, i_month)
                endDateStr = '{}-{}-01'.format(i_year, str(int(i_month) + 1))

            i_date = datetime.strptime(startDateStr, "%Y-%m-%d")
            endDate = datetime.strptime(endDateStr, "%Y-%m-%d")
            while i_date < endDate:
                i_date_str = i_date.strftime('%Y-%m-%d')
                # Add score "0" to null date
                if not df_all['PublishDate'].str.contains(i_date_str).any():
                    df_all.loc[-1] = [i_date_str,0]              # Append row to df_all, the index of it will be -1
                    df_all.reset_index(drop=True,inplace=True)
                    
                    
                i_date += timedelta(days=1)

            df_all = df_all.sort_values(by=['PublishDate'],ascending = True)
            df_all.to_csv('data/Step-3-A_SentimentScore/'+f'{category}_{i_year}{i_month}.csv', index=False)
            
            
                    
                        
sum_sentiment_score(marketKeyword,'market')
sum_sentiment_score(TSMCKeyword,'TSMC')
sum_sentiment_score(antiTSMCKeyword,'antiTSMC')



