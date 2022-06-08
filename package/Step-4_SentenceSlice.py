"""
Cut article into sentences and store the sentences in the company csv file (all dates in a file)
in structured direcotory (in ./data/Step-4_SentenceSliced/)
"""
import os
import pandas as pd 
from datetime import datetime

symbol_id = 2330
stockCodeDF = pd.read_csv('./data/Step-3_StockCodeList.csv')

# Log on terminal
def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ", something)


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



# This is official function, please don't forget to recover it
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
        i_stockId = stockCodeDF['stock_id'][i]

        if (i_stockName in sentence) or (i_stockId in sentence):
            # print('This is {}({}) news'.format(i_stockName,i_stockId))
            sentenceStockIndustryList.append(i_stockIndustry)
            sentenceStockNameList.append(i_stockName)
            sentenceStockIdLlist.append(i_stockId)
    return sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist
    
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
        path = 'data/Step-4_SentenceSliced/'
        file = '無產業分類_無股票ID_無公司.csv'
        dicto = {'PublishDate': [timestamp],
                 'Sentence': [sentence]}
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
            path = './data/Step-4_SentenceSliced/'
            file = f'{industry}_{stockId}_{name}.csv'
            dicto = {'PublishDate': [timestamp],
                     'Sentence': [sentence]}
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
# Main: Add sentence into csv
# =============================================================================
for i_year in range(2017,2022):
    for i_month in range(1,13):
        if i_month < 10 :
            i_month = '0' + str(i_month)
        else:
            i_month = str(i_month)
        newsDF = pd.read_csv('./data/Step-3_2330HistoryNews/news_2330_{}{}.csv'.format(i_year,i_month))
        for i_article in range(len(newsDF)):
            article = newsDF['content'][i_article]
            timestamp = newsDF['timestamp'][i_article]
            if isinstance(article, float):
                write_log('No article.')
                continue
            sentenceList = sentence_slice(article)
            for i_sentence in range(len(sentenceList)):
                sentence = sentenceList[i_sentence]
                sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist = sentence_check_company(sentence,stockCodeDF)
                save_sentence_to(sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist, timestamp, sentence)
                # write_log('')
                # write_log(sentence)
                # write_log(f'The {i_sentence} sentence in {i_article} article ' +
                #           f'at {i_year}-{i_month}-{timestamp[8:10]} has added into: ')
                #
write_log('the End')

'''
# =============================================================================
# Manually manipulate only
# =============================================================================
"""
Collect sentences into specific keyword file.
When you want to use these functions, move them onto main function.
"""

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
    stockCodeDF = pd.DataFrame({'industry_category': ['無產業分類', '無產業分類'],
                                'stock_id':['TSMC', 'TSMC'],
                                'stock_name':['蘋果', '蘋概股']
                                })
    for i in range(len(stockCodeDF)):
        i_stockIndustry = stockCodeDF['industry_category'][i]
        i_stockName = stockCodeDF['stock_name'][i]
        i_stockId = stockCodeDF['stock_id'][i]

        if (i_stockName in sentence) or (i_stockId in sentence):
            # print('This is {}({}) news'.format(i_stockName,i_stockId))
            sentenceStockIndustryList.append(i_stockIndustry)
            sentenceStockNameList.append(i_stockName)
            sentenceStockIdLlist.append(i_stockId)
    return sentenceStockIndustryList, sentenceStockNameList, sentenceStockIdLlist

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
        pass

    # Store sentence into relative companies file
    else:
        for industry, stockId, name in zip(sentenceStockIndustryList, sentenceStockIdLlist, sentenceStockNameList):
            path = './data/Step-4_SentenceSliced/'
            file = f'{industry}_{stockId}_{name}.csv'
            dicto = {'PublishDate': [timestamp],
                     'Sentence': [sentence]}
            oneRow = pd.DataFrame(dicto)
            if not os.path.exists(path + file):
                oneRow.to_csv(path+file, encoding='utf-8', index=False)
            else:
                rows = pd.read_csv(path + file,encoding='utf-8')
                wholeRows = pd.concat([rows, oneRow], ignore_index=True)
                wholeRows.to_csv(path + file, encoding='utf-8', index=False)
            # write_log(file)
'''