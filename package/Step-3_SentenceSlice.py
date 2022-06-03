# -*- coding: utf-8 -*-
'''
1. 取一個月份
2. 取一個文章
3. 取一個句子
4. 將句子存放在 "公司/公司-年月.csv",{'timestamp':'xxxx-xx-xx','sentence':'句子內容'

'''
import os 
import pandas as pd 
from datetime import datetime, timedelta

rootDirect = 'C:/Users/Vivian/Desktop/資訊碩士/資訊碩二上/畢業論文研究/StockPrediction'
os.chdir(rootDirect)
         
stockListPath = 'data/News/'
newsListPath = 'data/News/Step-3_2330HistoryNews/'
aggregateDict = 'data/Sentimental Feature/aggregation_dictionary/'




dataset = pd.read_csv(newsListPath+'news_2330_201701.csv')
article = dataset['content'][4]
timestamp = dataset['timestamp'][4]


marketKeyword = ['台股','大盤','外資','投信','自營商','法人','加權指數','美股','台灣','美國',
                 '景氣',]
TSMCKeyword = ['半導體','電子','晶圓','台積電','奈米','英特爾']
otherKeyword = ['金融','鋼鐵','三星','中國','大陸','避險','自行買賣',
                '會計師','分析師',]

def RecoverStockListFile():
    
    from FinMind.data import DataLoader
    api = DataLoader()
    # api.login_by_token(api_token='token')
    # api.login(user_id='user_id',password='password')
    df = api.taiwan_stock_info()
    df['stock_name'] = df['stock_name'].apply(lambda x: x.replace('*','')   if '*' in x else x)
    df.to_csv(stockListPath+'Step-3_StockCodeList.csv', encoding='utf-8',index=False)
RecoverStockListFile()


def AddNameInStockList(new_industry,new_stock_id,new_name):
    # check whether the new_name in stockList
    # https://stackoverflow.com/questions/30944577/check-if-string-is-in-a-pandas-dataframe
    # wetherInDf = stockList['stock_name'].str.contains(new_name).any() #fuzzy search
    stockList = pd.read_csv(stockListPath+'Step-3_StockCodeList.csv')
    wetherInDf = stockList['stock_name'].str.fullmatch(new_name).any()  #full match
    if wetherInDf:
        print('{} is already in df'.format(new_name))
    else:
        print('Adding {} into list...'.format(new_name))
        dicto = {}
        keys = stockList.columns.tolist()
        listo = [new_industry,new_stock_id,new_name,' ',' ']
        for i in range(len(keys)):
            dicto[keys[i]] = [listo[i]]
        new_df = pd.concat(([stockList,pd.DataFrame(dicto)]),ignore_index=True)
        new_df.to_csv(stockListPath+'Step-3_StockCodeList.csv', encoding='utf-8',index=False)


for market in marketKeyword:
    AddNameInStockList('無產業分類','market',market)

for TSMC in TSMCKeyword:
    AddNameInStockList('無產業分類','TSMC',TSMC)
    
for other in otherKeyword:
    AddNameInStockList('無產業分類','other',other)

stockList = pd.read_csv(stockListPath+'Step-3_StockCodeList.csv')


# In[]
import os 
import pandas as pd 
from datetime import datetime, timedelta
import math
import logging

rootDirect = 'C:/Users/Vivian/Desktop/資訊碩士/資訊碩二上/畢業論文研究/StockPrediction'
os.chdir(rootDirect)

symbol_id = 2330
stockListPath = 'data/News/'
newsListPath = 'data/News/Step-3_2330HistoryNews/'
aggregateDict = 'data/Sentimental Feature/aggregation_dictionary/'
stockList = pd.read_csv(stockListPath+'Step-3_StockCodeList.csv')






def setup_log(name):
    logger = logging.getLogger(name)   # > set up a new name for a new logger

    logger.setLevel(logging.DEBUG)  # here is the missing line
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    path = f'data/Logs/{name}'
    filename = f"{path}/{name}_{datetime.now():%Y-%m-%d}.log"
    
    if not  os.path.exists(path):
        os.makedirs(path)
    
    
    log_handler = logging.FileHandler(filename)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_format)

    logger.addHandler(log_handler)

    return logger



def SentenceSlice(article):
    '''input: article  output:sentencelist'''
    pointer = 0
    sentenceList = []
    for i in range(len(article)):
        if '】' == article[i:i+1]:
            pointer = i+1
        if '。' == article[i:i+1]:
            sentence = article[pointer: i+1]
            sentenceList.append(sentence)
            # print(sentence+'\n\n')
            
            # iterate
            pointer = i+1
    return sentenceList

# sentenceList = SentenceSlice(article)
# sentence = sentenceList[10]

def SentenceCheckCompany(sentence,stockList):
    '''input: sentence  output:台積電(2330)'''
    sentence_stockIndustry_list = []
    sentence_stockName_list = []
    sentence_stock_id_list = []
    for i in range(len(stockList)):
        i_stockIndustry = stockList['industry_category'][i]
        i_stockName = stockList['stock_name'][i]
        i_stock_id =  stockList['stock_id'][i]
        
        
        if (i_stockName in sentence) or (i_stock_id in sentence) :
            # print('This is {}({}) news'.format(i_stockName,i_stock_id))
            sentence_stockIndustry_list.append(i_stockIndustry)
            sentence_stockName_list.append(i_stockName)
            sentence_stock_id_list.append(i_stock_id)
    return sentence_stockIndustry_list, sentence_stockName_list, sentence_stock_id_list
    
# sentence_stockName_list, sentence_stock_id_list = SentenceCheckCompany(sentence)
        


def CalSentimentScore(sentence):
    '''input: sentence  output:int'''
    score = 0
    with open(aggregateDict+'Step-4_SelfNegative.txt',mode = 'r',encoding= 'utf-8') as file:
        neg = file.read().split('\n')
    for i in neg:
        if (i in sentence) and (i != '') :
            # print('neg'+i)
            score -= 1
    with open(aggregateDict+'Step-4_SelfPositive.txt',mode = 'r',encoding= 'utf-8') as file:
        pos = file.read().split('\n')
    for i in pos:
        if ( i in sentence) and (i != '') :
            # print('pos'+i)
            score += 1
    return score
            
# sentimentScore =  CalSentimentScore(sentence)       


def SaveSentenceTo(sentence_stockIndustry_list, sentence_stockName_list, sentence_stock_id_list, timestamp,sentence):
    if sentence_stockIndustry_list == []:
        path = 'data/Step-4_SentenceSliced/{}/{}_{}/'.format('無提到公司','無股票ID','無公司')
        file = '{}{}_{}_{}.csv'.format(timestamp[:4],timestamp[5:7],'無股票ID','無公司')
        if not os.path.exists(path):
                os.makedirs(path)
        dicto = {'PublishDate': [timestamp],
                     'Sentence':[sentence],
                     'Score':[CalSentimentScore(sentence)]}
        oneRow = pd.DataFrame(dicto)
        if not os.path.exists(path + file):
            oneRow.to_csv(path+file,encoding='utf-8',index=False)
        else:
            rows = pd.read_csv(path + file,encoding='utf-8')
            wholeRows = pd.concat([rows,oneRow], ignore_index=True)
            wholeRows.to_csv(path + file, encoding='utf-8', index=False)
        logger.info(file)
        
    else:
        for industry, stockid, name in zip(sentence_stockIndustry_list, sentence_stock_id_list,sentence_stockName_list): 
            path = 'data/Step-4_SentenceSliced/{}/{}_{}/'.format(industry,stockid,name)
            file = '{}{}_{}_{}.csv'.format(timestamp[:4],timestamp[5:7],stockid,name)
            if not os.path.exists(path):
                os.makedirs(path)
            dicto = {'PublishDate': [timestamp],
                         'Sentence':[sentence],
                         'Score':[CalSentimentScore(sentence)]}
            oneRow = pd.DataFrame(dicto)
            if not os.path.exists(path + file):
                oneRow.to_csv(path+file,encoding='utf-8',index=False)
            else:
                rows = pd.read_csv(path + file,encoding='utf-8')
                wholeRows = pd.concat([rows,oneRow], ignore_index=True)
                wholeRows.to_csv(path + file, encoding='utf-8', index=False)
            logger.info(file)
            
# SaveSentenceTo(sentence_stockName_list, sentence_stock_id_list, timestamp,sentence)


# =============================================================================
# 將sentence加入檔案
# =============================================================================


logger = setup_log(__file__.split('\\')[-1][:-3])


for i_year in range(2018,2019):
    for i_month in range(12,13):
        if i_month < 10 :
            i_month = '0' + str(i_month)
        else:
            i_month = str(i_month)
        dataset = pd.read_csv(newsListPath+'news_2330_{}{}.csv'.format(i_year,i_month))
        for i_article in range(len(dataset)):
            article = dataset['content'][i_article]
            timestamp = dataset['timestamp'][i_article]
            if isinstance(article, float):
                logger.info('No article.')
                continue
            sentenceList = SentenceSlice(article)
            # for i_sentence in range(len(sentenceList)):
            for i_sentence in range(len(sentenceList)):
                sentence = sentenceList[i_sentence]
                sentence_stockIndustry_list, sentence_stockName_list, sentence_stock_id_list = SentenceCheckCompany(sentence,stockList)
                SaveSentenceTo(sentence_stockIndustry_list, sentence_stockName_list, sentence_stock_id_list, timestamp,sentence)
                logger.info('The {} sentence in {} article at {}-{}-{} has added into: '.format(i_sentence,i_article,i_year,i_month,timestamp[8:10]))
                

# =============================================================================
# 移除特定月份檔案
# =============================================================================


# logger = setup_log(__file__.split('\\')[-1][:-3]+'_delete')
# print(os.getcwd())

# for i_year in range(2019,2020):
#     for i_month in range(1,2):
#         if i_month < 10 :
#             i_month = '0' + str(i_month)
#         else:
#             i_month = str(i_month)
#         dataset = pd.read_csv(newsListPath+'news_2330_{}{}.csv'.format(i_year,i_month))
#         for i_article in range(len(dataset)):        
#             article = dataset['content'][i_article]
#             timestamp = dataset['timestamp'][i_article]
#             if isinstance(article, float):
#                 logger.info('No article.')
#                 continue
#             sentenceList = SentenceSlice(article)
#             for i_sentence in range(len(sentenceList)):
#                 sentence = sentenceList[i_sentence]
#                 sentence_stockIndustry_list, sentence_stockName_list, sentence_stock_id_list = SentenceCheckCompany(sentence,stockList)
                
              
#                 if sentence_stockIndustry_list == []:
#                     path = 'data/Step-4_SentenceSliced/{}/{}_{}/'.format('無提到公司','無股票ID','無公司')
#                     file = '{}{}_{}_{}.csv'.format(timestamp[:4],timestamp[5:7],'無股票ID','無公司')
#                     if os.path.exists(path+file):
#                         os.remove(path+file)
#                         logger.info('Delete file: '+path+file)
#                 else:
#                     for industry, stockid, name in zip(sentence_stockIndustry_list, sentence_stock_id_list,sentence_stockName_list): 
#                         path = 'data/Step-4_SentenceSliced/{}/{}_{}/'.format(industry,stockid,name)
#                         file = '{}{}_{}_{}.csv'.format(timestamp[:4],timestamp[5:7],stockid,name)
#                         if os.path.exists(path+file):
#                             os.remove(path+file)
#                             logger.info('Delete file: '+path+file)