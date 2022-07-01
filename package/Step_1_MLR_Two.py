"""
Recursive training model depend on the units of layer.
When find out the observed models, iterate diffrent model parameters except of the units of layer.

"""
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


def CombData(pred, count):
    # 在前95%的交易日中，設定預測結果和收盤價一致
    sameDays = len(datasetDf) - len(pred)  # 預測結果和收盤價一致的天數
    datasetDf.loc[:, 'predictedValue'] = datasetDf.loc[:,
                                         'close']  # 預測結果跟收盤價一致，所以複製DataFrame的close欄數值，並貼上到df新宣告的predictedValue欄

    # 在後5%的交易日中，用測試集推算預測股價，用預測的資料蓋掉原後5%的資料
    datasetDf.loc[sameDays:, 'predictedValue'] = pred
    # datasetDf[['date', 'close', 'predictedValue']].to_csv(f'./data/Step_0_MLR_Two_Accuracy/Step_0_MLR_Two_Accuracy_{count}.csv', encoding='big5',
    #                                                       index=False)


def PltCombData(i_dataset, count):
    pltStart = i_dataset - 20  # int(len(datasetDf) * 9 / 10)

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
    plt.savefig(f'./data/Step_0_MLR_Two_png/Step_0_MLR_Two_Result_{count}.png')
    plt.close()  # prevent matplotlib auto plot
    # plt.show()


if __name__ == '__main__':
    # ==================================================================================================================
    # Prepare dataset
    allDatasetDf = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
    mask = allDatasetDf['date'].isin(['2021-01-03'])     # Predict from 2021-01-03
    startIdx = mask[mask].index.tolist()[0] + 10         # Plus 10 make it start from 2021-01-03
    modulo = len(allDatasetDf) % 10

    count = 0  # Set loop stop point
    rmseList = []
    # Ensure data at last duration be predicted: (len(allDatasetDf) + 10)
    for i_dataset in range(startIdx, len(allDatasetDf) + 10, 10):
        # if count >= 1:
        #     break
        # Ensure data at last duration be predicted
        isLastDuration = i_dataset > len(allDatasetDf)
        if isLastDuration:
            i_dataset = len(allDatasetDf) - 1
            datasetDf = allDatasetDf.loc[:i_dataset, ]
            startDate = datasetDf["date"][i_dataset - modulo]
            endDate = datasetDf["date"][i_dataset]

            print(f'{"=" * 20} predict date {startDate} ~ {endDate} {"=" * 20} ')

            new_feature = datasetDf.iloc[:, ~datasetDf.columns.isin(['date', 'close'])]
            new_target = np.array(datasetDf['close'])

            test_size = modulo / len(new_target)

        else:
            datasetDf = allDatasetDf.loc[:i_dataset, ]
            startDate = datasetDf["date"][i_dataset - 10]  # Predict from this date at this time
            endDate = datasetDf["date"][i_dataset]  # Predict from this date at this time

            print(f'{"=" * 20} predict date {startDate} ~ {endDate} {"=" * 20} ')

            # Select all rows, all columns except date and close as feature
            new_feature = datasetDf.iloc[:, ~datasetDf.columns.isin(['date', 'close'])]
            # Select close price as target
            # "Func: train_test_split" must input DataFrame or numpy array,
            # Turn pd.Series into np.array.
            new_target = np.array(datasetDf['close'])

            test_size = 10 / len(new_target)  # Split last 10 days into test dataset

        feature_train, feature_test, target_train, target_test = train_test_split(new_feature, new_target,
                                                                                  test_size=test_size,
                                                                                  shuffle=False)


        scaler = MinMaxScaler()
        feature_train_scaled = scaler.fit_transform(feature_train)
        feature_test_scaled = scaler.transform(feature_test)


        # ==================================================================================================================
        # Train model
        t0 = time.time()
        model = LinearRegression()  # 使用線性模型裡面的線性回歸
        model.fit(feature_train_scaled, target_train)
        params = model.get_params()
        print(params)

        pred = model.predict(feature_test_scaled)

        CombData(pred, count)
        # PltCombData(i_dataset, count)

        rmse = mean_squared_error(target_test, pred, squared=False)
        rmseList.append(float("{:.4f}".format(rmse)))

        count += 1

