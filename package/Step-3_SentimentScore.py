import pandas  as pd

df = pd.read_csv('data/News/Step-3_StockCodeList.csv')


with open('data/News/stock_company.txt','w') as file:
    for i in df['stock_name']:
        file.write(i+'\n')
    
    
# In[]


import os
rootDirect = 'D:\StockPrediction_ClearView'
os.chdir(rootDirect)
import pandas as pd
import time
from ckiptagger import WS, POS, NER
from ckiptagger import construct_dictionary
import logging
from datetime import datetime, timedelta
t0 = time.time()

ws = WS(r".\data\Sentimental Feature\Step-3_CKIPtaggerModule\data")
pos = POS(r".\data\Sentimental Feature\Step-3_CKIPtaggerModule\data")
ner = NER(r".\data\Sentimental Feature\Step-3_CKIPtaggerModule\data")
newsListPath = 'data/News/Step-3_2330HistoryNews/'





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


# =============================================================================
# 自建字典
# =============================================================================

# recommend_dictionary
with open('data/Sentimental Feature/aggregation_dictionary/Step-4_SelfPositive.txt',mode='r',encoding='utf-8') as file:
    terms = file.read().split('\n')
positiveDf = pd.DataFrame({'positive':[i for i in terms]})
positive_dict = {i:1 for i in terms}


with open('data/Sentimental Feature/aggregation_dictionary/Step-4_SelfNegative.txt',mode='r',encoding='utf-8') as file:
    terms = file.read().split('\n')
negativeDf = pd.DataFrame({'negative':[i for i in terms]})
negative_dict = {i:1 for i in terms}

positive_dict.update(negative_dict)
recommend_dictionary = positive_dict
recommend_dictionary = construct_dictionary(recommend_dictionary)


# coerce_dictionary
df = pd.read_csv('data/News/Step-3_StockCodeList.csv')
coerce_dictionary = dict((i,1) for i in df['stock_name'])
coerce_dictionary = construct_dictionary(coerce_dictionary)




moduleName = __file__.split('\\')[-1][:-3]

logger = setup_log(moduleName)

t1 = time.time()
logger.info(f'Prepare spending: {t1-t0:02f}')



timestampList=[]
scoreList=[]
for i_year in range(2017,2021):
    for i_month in range(1,13):
        if i_month < 10 :
            i_month = '0' + str(i_month)
        else:
            i_month = str(i_month)
        dataset = pd.read_csv(newsListPath+'news_2330_{}{}.csv'.format(i_year,i_month))
        for i_article in range(len(dataset)):
        # for i_article in range(0,1):
            t0 = time.time()
            article = dataset['content'][i_article]
            timestamp = dataset['timestamp'][i_article]
            if isinstance(article, float):
                logger.info('No article.')
                continue
            ws_result = ws([article]  ,
                            sentence_segmentation = True,
                            recommend_dictionary = recommend_dictionary,
                            coerce_dictionary = coerce_dictionary,
                            )
            score = positiveDf['positive'].isin(ws_result[0]).sum()-negativeDf['negative'].isin(ws_result[0]).sum()
            timestampList.append(timestamp[:10])
            scoreList.append(score)
            
            t1 = time.time()
            
            logger.info(timestamp)
            logger.info(f"Score: {score}")
            logger.info(positiveDf['positive'][positiveDf['positive'].isin(ws_result[0])].values.tolist())
            logger.info(negativeDf['negative'][negativeDf['negative'].isin(ws_result[0])].values.tolist())
            logger.info(f'Calculate score spending: {t1-t0:02f}')
            
            print(timestamp)
            print(f"Score: {score}")
            print(positiveDf['positive'][positiveDf['positive'].isin(ws_result[0])].values.tolist())
            print(negativeDf['negative'][negativeDf['negative'].isin(ws_result[0])].values.tolist())
            print(f'Calculate score spending: {t1-t0:02f}')
            
            
            
scoreTotalDf = pd.DataFrame({'PublishDate':timestampList,'Score':scoreList})
scoreTotalDf = scoreTotalDf.sort_values(by=['PublishDate'],ascending = True)
scoreTotalDf = scoreTotalDf.groupby(scoreTotalDf['PublishDate']).sum()
scoreTotalDf.reset_index(inplace=True)
scoreTotalDf.to_csv('data/Step-2_SentimentScore.csv', index=False)

            
            

