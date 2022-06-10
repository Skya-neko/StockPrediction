"""
Calculate sentiment score of all sentences, and sum them up daily.
Sum up daily sentiment score of TSMC ,antiTSMC, market categories,
then TSMC_score = TSMC - antiTSMC  
     market_score = market - antimarket
"""

import pandas as pd
import time
from ckiptagger import WS, POS, NER
from ckiptagger import construct_dictionary
from datetime import datetime, timedelta


ws = WS("../Step-3_CKIPtaggerModule/data")
pos = POS("../Step-3_CKIPtaggerModule/data")
ner = NER("../Step-3_CKIPtaggerModule/data")
sentenceListPath = './data/Step-4_SentenceSliced/'


# Log on terminal
def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ", something)


# =============================================================================
# Construct self-generating dictionary for ckiptagger used only
# =============================================================================
# Construct recommend dictionary
with open('./data/Step-4_SelfPositive.txt', mode='r', encoding='utf-8') as file:
    terms = file.read().split('\n')
positiveDf = pd.DataFrame({'positive': [i for i in terms]})    # Used to calculate sentiment score
positive_dict = {i: 1 for i in terms}

with open('./data/Step-4_SelfNegative.txt', mode='r', encoding='utf-8') as file:
    terms = file.read().split('\n')
negative_dict = {i: 1 for i in terms}
negativeDf = pd.DataFrame({'negative': [i for i in terms]})    # Used to calculate sentiment score

positive_dict.update(negative_dict)
recommend_dictionary = positive_dict
recommend_dictionary = construct_dictionary(recommend_dictionary)

# Construct coerce dictionary
df = pd.read_csv('./data/Step-3_StockCodeList.csv')
coerce_dictionary = dict((i, 1) for i in df['stock_name'])
coerce_dictionary = construct_dictionary(coerce_dictionary)





# =============================================================================
# Calculate score
# =============================================================================
def sum_category_score(categoryList,category):
    timestampList = []
    scoreList = []
    allKeywordScoreDF = pd.DataFrame()
    # Find out sentences_of_a_keyword.csv file name we want.
    stockCodeDF = pd.read_csv('./data/Step-3_StockCodeList.csv')
    categoryIdx = stockCodeDF['stock_name'].isin(categoryList)
    categoryInfoDF = stockCodeDF[categoryIdx]
    if category == 'TSMC':
        TSMCMask1 = categoryInfoDF['stock_name'].isin(['台積電'])
        TSMCMask2 = categoryInfoDF['industry_category'].isin(['電子工業'])
        TSMCMask = TSMCMask1 & TSMCMask2
        TSMCMaskIdx = TSMCMask[TSMCMask].index
        categoryInfoDF = categoryInfoDF.drop(TSMCMaskIdx)
    categoryInfoDF.reset_index(drop=True,inplace=True)
    for i_keyword in range(len(categoryInfoDF)):
        industry = categoryInfoDF['industry_category'][i_keyword]
        stockId = categoryInfoDF['stock_id'][i_keyword]
        keyword = categoryInfoDF['stock_name'][i_keyword]
        sentenceDF = pd.read_csv(f'./data/Step-4_SentenceSliced/{industry}_{stockId}_{keyword}.csv')
        # Calculate sentiment score of each sentence in sentences_of_a_keyword.csv
        for i_sentence in range(len(sentenceDF)):
            t0 = time.time()
            


            sentence = sentenceDF['Sentence'][i_sentence]
            ws_result = ws([sentence],                                   # Segment this sentence into words
                           sentence_segmentation=True,
                           recommend_dictionary=recommend_dictionary,
                           coerce_dictionary=coerce_dictionary,
                           )
            # if 台積電, 三星 are both in the sentence at the same time,
            # when it's turn to count 台積電 then count score,
            # when it's turn to count 三星 then ignore the sentence.
            if category == 'antiTSMC' and '台積電' in ws_result[0] and '三星' in ws_result[0]:
                print('continue')
                continue
            posIdx = positiveDf['positive'].isin(ws_result[0])           # Find out positive words index
            negIdx = negativeDf['negative'].isin(ws_result[0])           # Find out negative words index
            score = posIdx.sum() - negIdx.sum()                          # Calculate sentiment score
            scoreList.append(score)

            timestamp = sentenceDF['PublishDate'][i_sentence][:10]
            timestampList.append(timestamp)

            t1 = time.time()

        keywordScoreDF = pd.DataFrame({'PublishDate': timestampList, 'Score': scoreList})
        keywordScoreDF = keywordScoreDF.sort_values(by=['PublishDate'], ascending=True)
        keywordScoreDF = keywordScoreDF.groupby(keywordScoreDF['PublishDate']).sum()     # Sum the score at the same day
        keywordScoreDF.reset_index(inplace=True)    # After groupby function, PubilshDate will become index
        # keywordScoreDF.to_csv(f'./data/Step-2_CategorySentimentScore/Score_{industry}_{stockId}_{keyword}.csv',
        #                       index=False)

        if allKeywordScoreDF.empty:
            allKeywordScoreDF = keywordScoreDF
        else:
            allKeywordScoreDF = pd.concat([allKeywordScoreDF, keywordScoreDF], ignore_index=True)

    allKeywordScoreDF = allKeywordScoreDF.groupby(allKeywordScoreDF['PublishDate']).sum()  # Sum the score at the same day
    allKeywordScoreDF.reset_index(inplace=True)


    i_date = datetime.strptime('2017-01-01', "%Y-%m-%d")
    endDate = datetime.strptime('2021-12-31', "%Y-%m-%d")
    while i_date <= endDate:
        i_date_str = i_date.strftime('%Y-%m-%d')
        # Add score "0" to null date
        if not allKeywordScoreDF['PublishDate'].str.contains(i_date_str).any():
            allKeywordScoreDF.loc[len(allKeywordScoreDF)] = [i_date_str, 0]  # Append row to df_all, the index of it will be -1

        i_date += timedelta(days=1)

    allKeywordScoreDF = allKeywordScoreDF.sort_values(by=['PublishDate'], ascending=True)
    allKeywordScoreDF.to_csv(f'./data/Step-2_CategorySentimentScore/Score_{category}.csv', index=False)


def remove_dates_beyond(category, startDate, endDate):
    startDate = datetime.strptime(startDate, '%Y-%m-%d')
    endDate = datetime.strptime(endDate, '%Y-%m-%d')
    targetDF = pd.read_csv(f'./data/Step-2_CategorySentimentScore/Score_{category}.csv')
    targetDF['PublishDate'] = pd.to_datetime(targetDF['PublishDate'])
    mask = (targetDF['PublishDate'] > startDate) & (targetDF['PublishDate'] < endDate)
    targetDF = targetDF.loc[mask]
    # targetDF.to_csv(f'./data/Step-2_CategorySentimentScore/Score_{category}.csv', index=False)


def deduct_antiTSMC_score(categoryA, categoryB):
    categoryADF = pd.read_csv(f'./data/Step-2_CategorySentimentScore/Score_{categoryA}.csv')
    categoryBDF = pd.read_csv(f'./data/Step-2_CategorySentimentScore/Score_{categoryB}.csv')
    categoryADF['Anti-Score'] = categoryBDF['Score']
    categoryADF['FinalScore'] = categoryADF['Score'] - categoryADF['Anti-Score']
    categoryADF['Score'] = categoryADF['FinalScore']
    # categoryADF.drop(['Anti-Score', 'FinalScore'], axis=1)
    categoryADF.to_csv(f'./data/Step-2_CategorySentimentScore/Score_{categoryA}Mix.csv', index=False)

def sum_all_score(categoryList):
    categoryADF = pd.DataFrame()
    for i_category in categoryList:
        if categoryADF.empty:
            categoryADF = pd.read_csv(f'./data/Step-2_CategorySentimentScore/Score_{i_category}.csv')
        else:
            categoryBDF = pd.read_csv(f'./data/Step-2_CategorySentimentScore/Score_{i_category}.csv')
            categoryADF[f'{i_category}-Score'] = categoryBDF['Score']
    categoryADF['Score'] = categoryADF.sum(axis=1)
    categoryADF = categoryADF[['PublishDate', 'Score']]
    categoryADF.to_csv(f'./data/Step-2_CategorySentimentScore/Step-2_SentimentScore.csv', index=False)








# Category lists
marketKeyword = ['台股', '大盤', '外資', '投信', '自營商', '法人', '加權指數', '美股', '台灣', '美國', '景氣', ]
# the score of 台積電 will be doubled, because there are two 台積電 in the stockCodeDF
TSMCKeyword = ['半導體', '電子', '晶圓', '台積電', '奈米']
antiTSMCKeyword = ['三星', '英特爾']



# Run 1
# sum_category_score(marketKeyword, 'market')
# sum_category_score(TSMCKeyword, 'TSMC')
# sum_category_score(antiTSMCKeyword, 'antiTSMC')

# Run 2
# deduct_antiTSMC_score('TSMC', 'antiTSMC')

# Run 3
# sum_all_score(['TSMCMix', 'market'])




