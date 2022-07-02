import pandas as pd
import matplotlib.pyplot as plt

# modelFile = 'Step_0_ANN_One_Accuracy.csv'
# modelFile = 'Step_0_MLR_One_Accuracy.csv'
modelFile = 'Step_0_ANN_Two_Accuracy.csv'

predictDF = pd.read_csv('./data/'+modelFile, encoding='big5', index_col=False)
pltStart = int(len(predictDF) * 7.5 / 10)

plt.figure(figsize=(25, 10))
plt.title('Artificial Neural Network', fontsize=25)
predictDF['close'][pltStart:].plot(color='blue', label='Real Data')
predictDF['predictedValue'][pltStart:].plot(color='red', label='predicted Data')
plt.legend(loc='best', fontsize=18)

# 設定x座標的標籤
count10 = predictDF[pltStart:].index % 10 == 0  # 返回True False陣列
major_index = predictDF[pltStart:].index[count10]
major_xtics = predictDF['date'][pltStart:][major_index]  # 這邊的major_index換成count10也可以唷
plt.xticks(major_index, major_xtics, fontsize=16)  # 參數1填入刻度位，參數2填入於該刻度的標籤
plt.setp(plt.gca().get_xticklabels(), rotation=30)  # 旋轉x軸標籤，以免每一個都是橫的顯示會看不清楚

# 設定樣式
plt.grid(linestyle='-.')  # 在圖上顯示網底
plt.savefig('./data/Step_0_ANN_Two_Result.png')
plt.show()
