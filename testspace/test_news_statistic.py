import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
path = 'data/Step-3_2330HistoryNews/'

i_date = datetime.datetime.strptime('201701', '%Y%m')
endDate = datetime.datetime.strptime('202112', '%Y%m')
count = 0
while i_date <= endDate:
    fileName = f'news_2330_{i_date.strftime("%Y%m")}.csv'
    print(fileName)


    newsDF = pd.read_csv(path+fileName, encoding='utf-8', index_col=False)
    if count == 0:
        allNewsDF = newsDF
    else:
        allNewsDF = pd.concat([allNewsDF, newsDF], ignore_index=True)

    i_date += relativedelta(months=1)
    count += 1

allNewsDF['source'].value_counts()