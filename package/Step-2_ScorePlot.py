import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
filePath = 'data/'
file = 'Step_1_Dataset.csv'
data = pd.read_csv(filePath+file, encoding='big5')

# data['PublishDate'] = data['PublishDate'].dt.strftime("%Y-%m-%d")             #為了讓plt時的xlabel不要顯示00:00:00

plt.figure(figsize=(25,10))
plt.title('Sentiment Score Distribution',fontsize=25)
data['Score'].plot(color='blue', label='Score',style='.')
plt.legend(loc='best',fontsize=18)


count10 = data.index%100==0                          #返回True False陣列
major_index=data.index[count10]
major_xtics=data['date'][major_index]
plt.xticks(major_index, major_xtics,fontsize=16)                #參數1填入刻度位，參數2填入於該刻度的標籤
plt.setp(plt.gca().get_xticklabels(),rotation=30)   #旋轉x軸標籤，以免每一個都是橫的顯示會看不清楚

#設定樣式
plt.grid(linestyle='-.')                            #在圖上顯示網底
plt.savefig('./data/Step_1_SentimentScoreDistribution.png')
plt.show()