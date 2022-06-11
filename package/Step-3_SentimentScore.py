"""
Calculate sentiment score of all sentences, and sum them up daily.
Step-2_SentimentScore = TSMC_score - antiTSMC_score
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
df = pd.read_csv('./data/Step-4_StockCodeList.csv')
coerce_dictionary = dict((i, 1) for i in df['stock_name'])
coerce_dictionary = construct_dictionary(coerce_dictionary)





# =============================================================================
# Calculate score
# =============================================================================
def sum_category_score(filename, category):
    """
    Sum up sentiment score in the sentence, remove dates beyond we need and fill up null value.
    :param filename: Sentence file.
    :param category: Category of the sentence file.
    :return: None
    """
    timestampList = []
    scoreList = []
    scoreDF = pd.DataFrame()

    sentenceDF = pd.read_csv(filename)
    # Calculate sentiment score of each sentence in sentences_of_a_keyword.csv
    for i_sentence in range(len(sentenceDF)):
        t0 = time.time()

        sentence = sentenceDF['Sentence'][i_sentence]
        ws_result = ws([sentence],                                   # Segment this sentence into words
                       sentence_segmentation=True,
                       recommend_dictionary=recommend_dictionary,
                       coerce_dictionary=coerce_dictionary,
                       )
        posIdx = positiveDf['positive'].isin(ws_result[0])           # Find out positive words index
        negIdx = negativeDf['negative'].isin(ws_result[0])           # Find out negative words index
        score = posIdx.sum() - negIdx.sum()                          # Calculate sentiment score
        scoreList.append(score)

        timestamp = sentenceDF['PublishDate'][i_sentence][:10]
        timestampList.append(timestamp)

        t1 = time.time()

    scoreDF = pd.DataFrame({'PublishDate': timestampList, 'Score': scoreList})
    scoreDF = scoreDF.sort_values(by=['PublishDate'], ascending=True)
    scoreDF = scoreDF.groupby(scoreDF['PublishDate']).sum()    # Sum the score at the same day
    scoreDF.reset_index(inplace=True)                          # After groupby function, PubilshDate will become index

    i_date = datetime.strptime('2017-01-01', "%Y-%m-%d")
    endDate = datetime.strptime('2021-12-31', "%Y-%m-%d")

    # Remove days beyond the duration we want
    scoreDF['PublishDate'] = pd.to_datetime(scoreDF['PublishDate'])
    mask = (scoreDF['PublishDate'] >= i_date) & (scoreDF['PublishDate'] <= endDate)
    scoreDF = scoreDF.loc[mask]
    scoreDF['PublishDate'] = scoreDF['PublishDate'].dt.strftime('%Y-%m-%d')

    # Add score "0" to the dates which value is null
    while i_date <= endDate:
        i_date_str = i_date.strftime('%Y-%m-%d')
        if not scoreDF['PublishDate'].str.contains(i_date_str).any():
            scoreDF.loc[len(scoreDF)] = [i_date_str, 0]  # Append row to df_all, the index of it will be -1

        i_date += timedelta(days=1)

    scoreDF = scoreDF.sort_values(by=['PublishDate'], ascending=True)
    scoreDF.to_csv(f'./data/Step-2_CategorySentimentScore/Score_{category}.csv', index=False)




def deduct_antiTSMC_score(categoryA, categoryB):
    """
    Sentiment score of TSMC deduct sentiment score ofantiTSMC.
    :param categoryA: TSMC
    :param categoryB: antiTSMC
    :return: None
    """
    categoryADF = pd.read_csv(f'./data/Step-2_CategorySentimentScore/Score_{categoryA}.csv')
    categoryBDF = pd.read_csv(f'./data/Step-2_CategorySentimentScore/Score_{categoryB}.csv')
    categoryADF['Anti-Score'] = categoryBDF['Score']
    categoryADF['FinalScore'] = categoryADF['Score'] - categoryADF['Anti-Score']
    categoryADF['Score'] = categoryADF['FinalScore']
    # categoryADF.drop(['Anti-Score', 'FinalScore'], axis=1)
    categoryADF.to_csv(f'./data/Step-2_SentimentScore.csv', index=False)


TSMCSentencesFile = './data/Step-4_SentenceSliced/TSMC_Sentences.csv'
antiTSMCSentencesFile = './data/Step-4_SentenceSliced/antiTSMC_Sentences.csv'

# Run 1
sum_category_score(TSMCSentencesFile, 'TSMC')
sum_category_score(antiTSMCSentencesFile, 'antiTSMC')

# Run 2
# deduct_antiTSMC_score('TSMC', 'antiTSMC')



