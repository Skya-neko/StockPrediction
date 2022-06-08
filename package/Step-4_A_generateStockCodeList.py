import pandas as pd

dataset = pd.read_csv('./data/Step-3_2330HistoryNews/news_2330_201701.csv')
article = dataset['content'][4]
timestamp = dataset['timestamp'][4]

marketKeyword = ['台股', '大盤', '外資', '投信', '自營商', '法人', '加權指數', '美股', '台灣', '美國', '景氣', ]
TSMCKeyword = ['半導體', '電子', '晶圓', '台積電', '奈米', '英特爾']
otherKeyword = ['金融', '鋼鐵', '三星', '中國', '大陸', '避險', '自行買賣', '會計師', '分析師', ]


def recover_stock_list_file():
    from FinMind.data import DataLoader
    api = DataLoader()
    # api.login_by_token(api_token='token')
    # api.login(user_id='user_id',password='password')
    df = api.taiwan_stock_info()
    df['stock_name'] = df['stock_name'].apply(lambda x: x.replace('*', '') if '*' in x else x)
    df.to_csv('./data/Step-3_StockCodeList.csv', encoding='utf-8', index=False)


recover_stock_list_file()


def add_name_in_stock_list(new_industry, new_stock_id, new_name):
    # check whether the new_name in stockCodeDF
    # https://stackoverflow.com/questions/30944577/check-if-string-is-in-a-pandas-dataframe
    # wetherInDf = stockCodeDF['stock_name'].str.contains(new_name).any() #fuzzy search
    stockCodeDF = pd.read_csv('./data/Step-3_StockCodeList.csv')
    wetherInDf = stockCodeDF['stock_name'].str.fullmatch(new_name).any()  # full match
    if wetherInDf:
        print('{} is already in df'.format(new_name))
    else:
        print('Adding {} into list...'.format(new_name))
        dicto = {}
        keys = stockCodeDF.columns.tolist()
        listo = [new_industry, new_stock_id, new_name, ' ', ' ']
        for i in range(len(keys)):
            dicto[keys[i]] = [listo[i]]
        new_df = pd.concat(([stockCodeDF, pd.DataFrame(dicto)]), ignore_index=True)
        new_df.to_csv('./data/Step-3_StockCodeList.csv', encoding='utf-8', index=False)


for market in marketKeyword:
    add_name_in_stock_list('無產業分類', 'market', market)

for TSMC in TSMCKeyword:
    add_name_in_stock_list('無產業分類', 'TSMC', TSMC)

for other in otherKeyword:
    add_name_in_stock_list('無產業分類', 'other', other)

stockCodeDF = pd.read_csv('./data/Step-3_StockCodeList.csv')

