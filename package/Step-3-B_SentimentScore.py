import pandas as pd
import time
from ckiptagger import WS, POS, NER
from ckiptagger import construct_dictionary
from datetime import datetime


ws = WS("../Step-3_CKIPtaggerModule/data")
pos = POS("../Step-3_CKIPtaggerModule/data")
ner = NER("../Step-3_CKIPtaggerModule/data")
newsListPath = './data/Step-3_2330HistoryNews/'


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




timestampList = []
scoreList = []
for i_year in range(2017, 2022):
    for i_month in range(1, 13):
        # Replace i_month value to meet news file name
        if i_month < 10:
            i_month = '0' + str(i_month)
        else:
            i_month = str(i_month)
        newsDF = pd.read_csv(newsListPath + 'news_2330_{}{}.csv'.format(i_year, i_month))

        for i_article in range(len(newsDF)):
            t0 = time.time()

            timestamp = newsDF['timestamp'][i_article][:10]
            timestampList.append(timestamp)

            article = newsDF['content'][i_article]
            if isinstance(article, float):                              # If article type == float express no article in this row
                write_log('No article.')
                continue
            ws_result = ws([article],                                   # Segment this article into words
                           sentence_segmentation=True,
                           recommend_dictionary=recommend_dictionary,
                           coerce_dictionary=coerce_dictionary,
                           )
            posIdx = positiveDf['positive'].isin(ws_result[0])          # Find out positive words index
            negIdx = negativeDf['negative'].isin(ws_result[0])          # Find out negative words index
            score = posIdx.sum() - negIdx.sum()                         # Calculate sentiment score
            scoreList.append(score)

            t1 = time.time()

            # Debugging
            # write_log(timestamp)
            # write_log(f"Score: {score}")
            # write_log(positiveDf['positive'][posIdx].values.tolist())
            # write_log(negativeDf['negative'][negIdx].values.tolist())
            # write_log(f'Calculate score spending: {(t1 - t0):.2f}')


scoreTotalDf = pd.DataFrame({'PublishDate': timestampList, 'Score': scoreList})
scoreTotalDf = scoreTotalDf.sort_values(by=['PublishDate'], ascending=True)
scoreTotalDf = scoreTotalDf.groupby(scoreTotalDf['PublishDate']).sum()           # Sum the score at the same day
scoreTotalDf.reset_index(inplace=True)
scoreTotalDf.to_csv('./data/Step-2-B_SentimentScore.csv', index=False)
