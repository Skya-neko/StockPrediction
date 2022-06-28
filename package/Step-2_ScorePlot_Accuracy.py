import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
datasetDF = datasetDF[['date', 'close', 'Score']]
# datasetDF = datasetDF.iloc[-100:,].reset_index(drop=True)
datasetDF['TP/TN'] = None
latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
closeSpread = latter - former
closeFirstDay = 183 - 181.5
closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)

TP = 0
TN = 0
FP = 0
FN = 0
# T: Correctly recognize the sample
# F: Uncorrectly recognize the sample
# P: the sample belongs to A category (stock price rise)
# N: the sample belongs to B category (stock price fall)



for i in range(len(closeSpread)):
    # Stock price rise
    if closeSpread[i] >= 0:
        if datasetDF['Score'][i] >= 0:
            TP += 1
            datasetDF['TP/TN'][i] = datasetDF['Score'][i]
            datasetDF['Score'][i] = None
        else:
            FP += 1
    # Stock price fall
    else:
        if datasetDF['Score'][i] < 0:
            TN += 1
            datasetDF['TP/TN'][i] = datasetDF['Score'][i]
            datasetDF['Score'][i] = None
        else:
            FN += 1

accuracy = (TP+TN) / (TP+TN+FP+FN)



# data['PublishDate'] = data['PublishDate'].dt.strftime("%Y-%m-%d")             #為了讓plt時的xlabel不要顯示00:00:00

plt.figure(figsize=(25,10))
plt.title('Sentiment Score Distribution (with TP/TN)',fontsize=25)
datasetDF['Score'].plot(color='blue', label='Score', style='.')
datasetDF['TP/TN'].plot(color='red', label='TP/TN Score', style='.')
plt.legend(loc='best',fontsize=18)


count10 = datasetDF.index%100==0                          #返回True False陣列
major_index=datasetDF.index[count10]
major_xtics=datasetDF['date'][major_index]
plt.xticks(major_index, major_xtics, fontsize=16)                #參數1填入刻度位，參數2填入於該刻度的標籤
plt.setp(plt.gca().get_xticklabels(), rotation=30)   #旋轉x軸標籤，以免每一個都是橫的顯示會看不清楚

#設定樣式
plt.grid(linestyle='-.')                            #在圖上顯示網底
plt.savefig('./data/Step_1_SentimentScoreDistribution_Accuracy.png')
plt.show()
