# =============================================================================
# import module
# =============================================================================
# 資料分析套件
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Normalization

from sklearn.preprocessing import MinMaxScaler

# sklearn MLP
from sklearn.metrics import mean_squared_error


#
# #keras MLP
# tf.compat.v1.disable_eager_execution()


def CombData(pred):
    # 在前95%的交易日中，設定預測結果和收盤價一致
    sameDays = len(datasetDf) - len(pred)  # 預測結果和收盤價一致的天數
    datasetDf.loc[:, 'predictedValue'] = datasetDf.loc[:,
                                         'close']  # 預測結果跟收盤價一致，所以複製DataFrame的close欄數值，並貼上到df新宣告的predictedValue欄

    # 在後5%的交易日中，用測試集推算預測股價，用預測的資料蓋掉原後5%的資料
    datasetDf.loc[sameDays:, 'predictedValue'] = pred


def PltCombData():
    pltStart = int(len(datasetDf) * 7 / 10)

    plt.figure(figsize=(25, 10))
    plt.title('Multiple Linear Regression', fontsize=25)
    datasetDf['close'][pltStart:].plot(color='blue', label='Real Data')
    datasetDf['predictedValue'][pltStart:].plot(color='red', label='predicted Data')
    plt.legend(loc='best', fontsize=18)

    # 設定x座標的標籤
    count10 = datasetDf[pltStart:].index % 10 == 0  # 返回True False陣列
    major_index = datasetDf[pltStart:].index[count10]
    major_xtics = datasetDf['date'][pltStart:][major_index]  # 這邊的major_index換成count10也可以唷
    plt.xticks(major_index, major_xtics, fontsize=16)  # 參數1填入刻度位，參數2填入於該刻度的標籤
    plt.setp(plt.gca().get_xticklabels(), rotation=30)  # 旋轉x軸標籤，以免每一個都是橫的顯示會看不清楚

    # 設定樣式
    plt.grid(linestyle='-.')  # 在圖上顯示網底
    # plt.savefig('./data/Step_0_MLROneResult.png')
    # plt.close()  # prevent matplotlib auto plot
    plt.show()


def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.ylim([0, 10])
    plt.xlabel('Epoch')
    plt.ylabel('Error [MPG]')
    plt.legend()
    plt.grid(True)
    plt.show()


print('執行case: ')
datasetDf = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')

# 劃分特徵值和目標值(都要變成ndarray才可以輸入train_test_split
feature = datasetDf.iloc[:,
          ~datasetDf.columns.isin(['date', 'close'])]  # 單獨抓出feature的值，並將其指定給feature。對df使用values函式後，資料型態就會變成ndarray
target = np.array(datasetDf['close'])  # 將df中的'close'欄位，存成numpy的array

# 劃分訓練集，測試集
feature_train, feature_test, target_train, target_test = train_test_split(feature, target, test_size=0.25,
                                                                          random_state=0, shuffle=False)

print(datasetDf.describe().transpose()[['mean', 'std']])
normalizer = Normalization(axis=-1)
# adapt to the data
normalizer.adapt(np.array(feature_train))
haha = normalizer.mean.numpy()

# When the layer is called it returns the input data, with each feature independently normalized:
# (input-mean)/stddev
first = np.array(feature_train[:1])
print('First example:', first)
print('Normalized:', normalizer(first).numpy())

# multiple inputs
linear_model = tf.keras.Sequential([
    normalizer,
    layers.Dense(units=1)  # Linear Model
])

linear_model.layers[1].kernel
linear_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')
history = linear_model.fit(
    feature_train,
    target_train,
    epochs=100,
    # Suppress logging.
    verbose=0,
    # Calculate validation results on 20% of the training data.
    validation_split=0.2)
# plot_loss(history)
print('yes')

pred = linear_model.predict(feature_test)
CombData(pred)
PltCombData()
