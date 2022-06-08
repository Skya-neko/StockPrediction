"""
Cut article into sentences and calculate sentence sentiment score, and store the sentences in the monthly csv file
in structured direcotory (in ./data/Step-4-A_SentenceSliced/)
"""
import os
import pandas as pd 
from datetime import datetime

symbol_id = 2330
stockCodeDF = pd.read_csv('./data/Step-3_StockCodeList.csv')

# Log on terminal
def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ",something)


def sentence_slice(article):
    """
    Divide article into sentences.
    :param article: a piece of news
    :return: sentencelist
    """
    pointer = 0
    sentenceList = []
    for i in range(len(article)):
        if '】' == article[i:i+1]:
            pointer = i+1
        if '。' == article[i:i+1] or '！' == article[i:i+1]:
            sentence = article[pointer: i+1]
            sentenceList.append(sentence)
            # print(sentence+'\n\n')
            pointer = i+1
    return sentenceList

# sentenceList = sentence_slice(article)
# sentence = sentenceList[10]

def sentence_check_company(sentence, 
                           stockCodeDF):
    """
    Find out this sentence mentions what companies.
    :param sentence: Target sentence we want to analyze.
    :param stockCodeDF: Find out companies according to this companies list.
    :return: sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist
    """
    sentenceStockIndustryList = []
    sentenceStockNameList = []
    sentenceStockIdLlist = []
    for i in range(len(stockCodeDF)):
        i_stockIndustry = stockCodeDF['industry_category'][i]
        i_stockName = stockCodeDF['stock_name'][i]
        i_stock_id =  stockCodeDF['stock_id'][i]
        
        
        if (i_stockName in sentence) or (i_stock_id in sentence) :
            # print('This is {}({}) news'.format(i_stockName,i_stock_id))
            sentenceStockIndustryList.append(i_stockIndustry)
            sentenceStockNameList.append(i_stockName)
            sentenceStockIdLlist.append(i_stock_id)
    return sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist
    
# sentenceStockNameList, sentenceStockIdLlist = sentence_check_company(sentence)
        


def cal_sentiment_score(sentence):
    """
    Calculate the sentiment score of a sentence.
    :param sentence: Target sentence we want to analyze.
    :return: score
    """
    score = 0
    with open('./data/Step-4_SelfNegative.txt',mode = 'r',encoding= 'utf-8') as file:
        neg = file.read().split('\n')
    for i in neg:
        if (i in sentence) and (i != '') :
            # print('neg'+i)
            score -= 1
    with open('./data/Step-4_SelfPositive.txt',mode = 'r',encoding= 'utf-8') as file:
        pos = file.read().split('\n')
    for i in pos:
        if ( i in sentence) and (i != '') :
            # print('pos'+i)
            score += 1
    return score
            
# sentimentScore =  cal_sentiment_score(sentence)


def save_sentence_to(sentenceStockIndustryList,
                     sentenceStockNameList,
                     sentenceStockIdLlist,
                     timestamp,
                     sentence):
    """
    Save sentence into relative {publishing-date:YYYYMM}_{company} file to do categorize.
    :param sentenceStockIndustryList: The industry mentioned in this sentence.
    :param sentenceStockNameList: The company name mentioned in this sentence.
    :param sentenceStockIdLlist: The stock code mentioned in this sentence.
    :param timestamp: The publishing date of the sentence.
    :param sentence: Target sentence we want to analyze.
    :return: None
    """
    # Store sentence which doesn't mention any company.
    if not sentenceStockIndustryList:
        path = 'data/Step-4-A_SentenceSliced/{}/{}_{}/'.format('無提到公司', '無股票ID', '無公司')
        file = '{}{}_{}_{}.csv'.format(timestamp[:4], timestamp[5:7], '無股票ID', '無公司')
        if not os.path.exists(path):
                os.makedirs(path)
        dicto = {'PublishDate': [timestamp],
                 'Sentence': [sentence],
                 'Score': [cal_sentiment_score(sentence)]}
        oneRow = pd.DataFrame(dicto)
        if not os.path.exists(path + file):
            oneRow.to_csv(path+file, encoding='utf-8', index=False)
        else:
            rows = pd.read_csv(path + file, encoding='utf-8')
            wholeRows = pd.concat([rows, oneRow], ignore_index=True)
            wholeRows.to_csv(path + file, encoding='utf-8', index=False)
        write_log(file)

    # Store sentence into relative companies file
    else:
        for industry, stockId, name in zip(sentenceStockIndustryList, sentenceStockIdLlist, sentenceStockNameList):
            path = './data/Step-4-A_SentenceSliced/{}/{}_{}/'.format(industry, stockId, name)
            file = '{}{}_{}_{}.csv'.format(timestamp[:4], timestamp[5:7], stockId, name)
            if not os.path.exists(path):
                os.makedirs(path)
            dicto = {'PublishDate': [timestamp],
                     'Sentence': [sentence],
                     'Score': [cal_sentiment_score(sentence)]}
            oneRow = pd.DataFrame(dicto)
            if not os.path.exists(path + file):
                oneRow.to_csv(path+file, encoding='utf-8', index=False)
            else:
                rows = pd.read_csv(path + file,encoding='utf-8')
                wholeRows = pd.concat([rows, oneRow], ignore_index=True)
                wholeRows.to_csv(path + file, encoding='utf-8', index=False)
            write_log(file)
            
# save_sentence_to(sentenceStockNameList, sentenceStockIdLlist, timestamp,sentence)


# =============================================================================
# Add sentence into csv
# =============================================================================
for i_year in range(2017,2019):
    for i_month in range(12,13):
        if i_month < 10 :
            i_month = '0' + str(i_month)
        else:
            i_month = str(i_month)
        newsDF = pd.read_csv('./data/Step-3_2330HistoryNews/'+'news_2330_{}{}.csv'.format(i_year,i_month))
        for i_article in range(len(newsDF)):
            article = newsDF['content'][i_article]
            timestamp = newsDF['timestamp'][i_article]
            if isinstance(article, float):
                write_log('No article.')
                continue
            sentenceList = sentence_slice(article)
            # for i_sentence in range(len(sentenceList)):
            for i_sentence in range(len(sentenceList)):
                sentence = sentenceList[i_sentence]
                sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist = sentence_check_company(sentence,stockCodeDF)
                save_sentence_to(sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist, timestamp,sentence)
                write_log('The {} sentence in {} article at {}-{}-{} has added into: '.format(i_sentence,i_article,i_year,i_month,timestamp[8:10]))
                

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
#         newsDF = pd.read_csv('./data/Step-3_2330HistoryNews/'+'news_2330_{}{}.csv'.format(i_year,i_month))
#         for i_article in range(len(newsDF)):        
#             article = newsDF['content'][i_article]
#             timestamp = newsDF['timestamp'][i_article]
#             if isinstance(article, float):
#                 write_log('No article.')
#                 continue
#             sentenceList = sentence_slice(article)
#             for i_sentence in range(len(sentenceList)):
#                 sentence = sentenceList[i_sentence]
#                 sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist = sentence_check_company(sentence,stockCodeDF)
                
              
#                 if sentenceStockIndustryList == []:
#                     path = 'data/Step-4-A_SentenceSliced/{}/{}_{}/'.format('無提到公司','無股票ID','無公司')
#                     file = '{}{}_{}_{}.csv'.format(timestamp[:4],timestamp[5:7],'無股票ID','無公司')
#                     if os.path.exists(path+file):
#                         os.remove(path+file)
#                         write_log('Delete file: '+path+file)
#                 else:
#                     for industry, stockId, name in zip(sentenceStockIndustryList, sentenceStockIdLlist,sentenceStockNameList): 
#                         path = 'data/Step-4-A_SentenceSliced/{}/{}_{}/'.format(industry,stockId,name)
#                         file = '{}{}_{}_{}.csv'.format(timestamp[:4],timestamp[5:7],stockId,name)
#                         if os.path.exists(path+file):
#                             os.remove(path+file)
#                             write_log('Delete file: '+path+file)