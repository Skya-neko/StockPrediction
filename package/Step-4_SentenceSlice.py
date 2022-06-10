"""
Cut article into sentences and store the sentences in the company csv file (all dates in a file)
in structured direcotory (in ./data/Step-4_SentenceSliced/)
"""
import os
import pandas as pd 
from datetime import datetime
from dateutil.relativedelta import relativedelta

symbol_id = 2330
stockCodeDF = pd.read_csv('./data/Step-4_StockCodeList.csv')

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
def sentence_check_company(sentence, stockCodeDF):
    """
    Find out this sentence mentions what companies.
    :param sentence: Target sentence we want to analyze.
    :param stockCodeDF: Find out companies according to this companies list.
    :return: sentenceCompaniesDF
    """
    sentenceStockNameList = []
    sentenceStockIdLlist = []
    for i in range(len(stockCodeDF)):
        i_stockName = stockCodeDF['stock_name'][i]
        i_stockId = stockCodeDF['stock_id'][i]

        if (i_stockName in sentence) or (i_stockId in sentence):
            # print('This is {}({}) news'.format(i_stockName,i_stockId))
            sentenceStockNameList.append(i_stockName)
            sentenceStockIdLlist.append(i_stockId)

    sentenceCompaniesDF = pd.DataFrame({
        'stock_name': sentenceStockNameList,
    })
    return sentenceCompaniesDF

def __save_sentence_iterate(path, file, oneRow):
    """
    This is for func: save_sentence_to use.
    :param path: path to save file
    :param file: file name to save file
    :param oneRow: a record, which is a DataFrame
    :return: None
    """
    if not os.path.exists(path + file):
        oneRow.to_csv(path + file, encoding='utf-8', index=False)
    else:
        rows = pd.read_csv(path + file, encoding='utf-8')
        wholeRows = pd.concat([rows, oneRow], ignore_index=True)
        wholeRows.to_csv(path + file, encoding='utf-8', index=False)
    # write_log(file)
    
def save_sentence_to(sentenceCompaniesDF, timestamp, sentence):
    """
    Save sentence into TSMC_Sentences file to do categorize.
    :param sentenceCompaniesDF: the keywords mentioned in the sentence.
    :param timestamp: The publishing date of the sentence.
    :param sentence: Target sentence we want to analyze.
    :return: None
    """
    marketKeyword = ['台股', '大盤', '外資', '投信', '自營商', '法人', '加權指數', '美股', '台灣', '美國', '景氣', ]
    TSMCKeyword = ['半導體', '電子', '晶圓', '台積電', '奈米']
    TSMCKeyword.extend(marketKeyword)
    antiTSMCKeyword = ['三星', '英特爾']

    # Find out what category the sentence is.
    mask = sentenceCompaniesDF['stock_name'].isin(TSMCKeyword)
    antiMask = sentenceCompaniesDF['stock_name'].isin(antiTSMCKeyword)

    path = 'data/Step-4_SentenceSliced/'
    dicto = {'PublishDate': [timestamp],
             'Sentence': [sentence]}
    oneRow = pd.DataFrame(dicto)

    # If the sentence belongs to both categories, then take TSMC as the major one.
    # For example, if 台積電, 三星 are both in the sentence at the same time,
    # when it's turn to count 台積電 then count score,
    # when it's turn to count 三星 then ignore the sentence.
    if mask.any() and antiMask.any():
        file = 'TSMC_Sentences.csv'
        __save_sentence_iterate(path, file, oneRow)

    elif mask.any():
        file = 'TSMC_Sentences.csv'
        __save_sentence_iterate(path, file, oneRow)

    elif antiMask.any():
        file = 'antiTSMC_Sentences.csv'
        __save_sentence_iterate(path, file, oneRow)



# =============================================================================
# Main: Add sentence into csv
# =============================================================================
i_date = datetime.strptime('2017-01-01', '%Y-%m-%d')
endDate = datetime.strptime('2021-12-31', '%Y-%m-%d')
while i_date < endDate:
    monthStr = i_date.strftime('%Y%m')
    newsDF = pd.read_csv('./data/Step-3_2330HistoryNews/news_2330_{}.csv'.format(monthStr))

    for i_article in range(len(newsDF)):
        article = newsDF['content'][i_article]
        timestamp = newsDF['timestamp'][i_article]
        if isinstance(article, float):
            write_log('No article.')
            continue
        sentenceList = sentence_slice(article)
        for i_sentence in range(len(sentenceList)):
            sentence = sentenceList[i_sentence]
            sentenceCompaniesDF = sentence_check_company(sentence, stockCodeDF)

            # Debug
            # write_log('')
            # write_log(sentence)
            # write_log(f'The {i_sentence} sentence in {i_article} article ' +
            #           f'at {monthStr}{timestamp[8:10]} has added into: ')

            save_sentence_to(sentenceCompaniesDF, timestamp, sentence)

    i_date += relativedelta(months=1)

write_log('the End')



