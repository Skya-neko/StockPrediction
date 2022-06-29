"""
Recursive training model depend on the units of layer.
When find out the observed models, iterate diffrent model parameters except of the units of layer.

"""
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import time
from tensorflow.compat.v1.keras import Sequential
from tensorflow.compat.v1.keras.layers import Dense
from tensorflow.compat.v1.keras.optimizers import SGD
from tensorflow.compat.v1 import set_random_seed
from tensorflow.keras.utils import plot_model

import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def CombData(datasetDf, pred):
    # 在前95%的交易日中，設定預測結果和收盤價一致
    sameDays = len(datasetDf) - len(pred)  # 預測結果和收盤價一致的天數
    # 預測結果跟收盤價一致，所以複製DataFrame的close欄數值，並貼上到df新宣告的predictedValue欄
    datasetDf['predictedValue'] = datasetDf['close']

    # 在後5%的交易日中，用測試集推算預測股價，用預測的資料蓋掉原後5%的資料
    datasetDf.loc[sameDays:, 'predictedValue'] = pred
    datasetDf[['date', 'close', 'predictedValue']].to_csv('./data/Step_0_ANN_One_Accuracy.csv', encoding='big5',
                                                          index=False)


def PltCombData(datasetDf):
    pltStart = int(len(datasetDf) * 7.5 / 10)

    plt.figure(figsize=(25, 10))
    plt.title('Artificial Neural Network', fontsize=25)
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
    # plt.savefig(self.outputFilePath+self.case+'.png')
    plt.show()

if __name__ == '__main__':

    paramDict = {
        # In tuning, random_seed is not important in statistic result
        'random_seed': 200,
        'Dense1Units': 40,
        'Dense2Units': 58,
        'learning_rate': 0.00001,
        'decay': 0.0,
        'momentum': 0.9,
        'nesterov': True,
        'optimizer': 'sgd',
        'loss': 'mean_squared_error',
        'epochs': 2000,
        'verbose': 0,
        'batch_size': 10,
    }


    # ==================================================================================================================
    # Prepare dataset
    datasetDf = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
    mask = datasetDf['date'].isin(['2021-01-03'])  # Predict from 2021-01-03
    startIdx = mask[mask].index.tolist()[0]
    startDate = datasetDf["date"][startIdx]
    endDate = datasetDf["date"].iloc[-1]

    print(f'{"=" * 20} predict date {startDate} ~ {endDate} {"=" * 20} ')

    # Select all rows, all columns except date and close as feature
    new_feature = datasetDf.iloc[:, ~datasetDf.columns.isin(['date', 'close'])]
    # Select close price as target
    # "Func: train_test_split" must input DataFrame or numpy array,
    # Turn pd.Series into np.array.
    new_target = np.array(datasetDf['close'])

    test_size = (len(datasetDf) - startIdx) / len(new_target)
    feature_train, feature_test, target_train, target_test = train_test_split(new_feature, new_target,
                                                                              test_size=test_size,
                                                                              shuffle=False)

    scaler = MinMaxScaler()
    feature_train_scaled = scaler.fit_transform(feature_train)
    feature_test_scaled = scaler.transform(feature_test)


    # ==================================================================================================================
    # Train model
    t0 = time.time()
    set_random_seed(paramDict['random_seed'])

    model = Sequential()
    model.add(Dense(units=paramDict['Dense1Units'], activation='relu',
                    input_dim=feature_train_scaled.shape[1], ))
    model.add(Dense(units=paramDict['Dense2Units'], activation='relu', ))
    model.add(Dense(units=1, ))

    sgd = SGD(learning_rate=paramDict['learning_rate'], decay=paramDict['decay'],
              momentum=paramDict['momentum'], nesterov=paramDict['nesterov'])

    model.compile(optimizer=sgd, loss=paramDict['loss'])
    model.fit(feature_train_scaled, target_train, epochs=paramDict['epochs'], verbose=paramDict['verbose'],
              batch_size=paramDict['batch_size'], shuffle=False)

    pred = model.predict(feature_test_scaled)
    score = model.evaluate(feature_test_scaled, target_test, verbose=1)
    model.summary()

    # Visualize result
    CombData(datasetDf, pred)
    PltCombData(datasetDf)

    # path = "./data./Step_0_model_plot_ANN_One.png"
    # plot_model(model, show_shapes=True, to_file=path)

    # count += 1

