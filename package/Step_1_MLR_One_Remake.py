import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
from memory_profiler import profile  # Memory Observation
import itertools
# from multiprocessing import Process, Queue
from sklearn.linear_model import LinearRegression


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import joblib  # Save sklearn scaler





# Log on terminal
def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ", something)

def CombData(datasetDf, pred):
    # 在前95%的交易日中，設定預測結果和收盤價一致
    sameDays = len(datasetDf) - len(pred)  # 預測結果和收盤價一致的天數
    # 預測結果跟收盤價一致，所以複製DataFrame的close欄數值，並貼上到df新宣告的predictedValue欄
    datasetDf['predictedValue'] = datasetDf['close']

    # 在後5%的交易日中，用測試集推算預測股價，用預測的資料蓋掉原後5%的資料
    datasetDf.loc[sameDays:, 'predictedValue'] = pred

    # datasetDf[['date', 'close', 'predictedValue']].to_csv('./data/Step_0_MLR_One_Accuracy.csv', encoding='big5', index=False)


def PltCombData(datasetDf):
    pltStart = int(len(datasetDf) * 7.5 / 10)

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
    # plt.savefig(self.outputFilePath+self.case+'.png')
    plt.show()


def new_param_dict(random_seed, Dense1Units,
                   Dense2Units, learning_rate,
                   decay,       momentum,
                   epochs,      batch_size):
    paramDict = {
        # In tuning, random_seed is not important in statistic result
        'random_seed': random_seed,
        'Dense1Units': Dense1Units,
        'Dense2Units': Dense2Units,
        'learning_rate': learning_rate,
        'decay': decay,
        'momentum': momentum,
        'nesterov': True,
        'optimizer': 'sgd',
        'loss': 'mean_squared_error',
        'epochs': epochs,
        'verbose': 0,
        'batch_size': batch_size,
    }
    return paramDict



# @profile   # uncomment for memory obervation & don't use in debugger mode
def main():


    datasetDf = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
    mask = datasetDf['date'].isin(['2021-01-03'])     # Predict from 2021-01-03
    startIdx = mask[mask].index.tolist()[0]
    startDate = datasetDf["date"][startIdx]
    endDate = datasetDf["date"].iloc[-1]



    write_log(f'{"=" * 20} predict date {startDate} ~ {endDate} {"=" * 20} ')

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

    scaler = joblib.load('./data/Step_1_ANN_One_Scaler.gz')
    feature_train_scaled = scaler.fit_transform(feature_train)
    feature_test_scaled = scaler.transform(feature_test)





    t0 = time.time()
    model = LinearRegression()  # 使用線性模型裡面的線性回歸
    model.fit(feature_train_scaled, target_train)
    params = model.get_params()
    print(params)

    pred = model.predict(feature_test_scaled)




    score = None


    # Visualize result
    # CombData(datasetDf, pred)
    # PltCombData(datasetDf)


    # Save result
    try:
        rmse = mean_squared_error(target_test, pred, squared=False)
        write_log(rmse)
        rmseStr = str(rmse)[:7].replace('.', '_')

        t1 = time.time()

        outputFileName = f'rmseBeyond{limit}'

        if rmse < limit:
            outputFileName = 'keras_' + rmseStr + '.h5'

        recordDict = {
            'modelName': outputFileName,
            'score': score,
            'rmse': rmse,
            'spendTime': t1 - t0,
            'executionTime': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'startDate': startDate,
            'endDate': endDate,
        }
        # write_log('Output')
        # write_log(str(recordDict).replace(', ', ',\n').replace("{'", "{\n'").replace("}", "\n}"))
        # recordDict.update(paramDict)
        # rowDf = pd.DataFrame([recordDict], columns=recordDict.keys())
        #
        # # Initialize record file
        # # rowDf.to_csv(outputFilePath+recordFileName, encoding='big5', index=False)
        # # recordDf = pd.read_csv(outputFilePath+recordFileName, index_col=False).head(0)
        #
        # recordDf = pd.read_csv(outputFilePath + recordFileName, index_col=False)
        # recordDf = pd.concat([recordDf, rowDf], axis=0).reset_index(drop=True)
        # recordDf.to_csv(outputFilePath + recordFileName, encoding='big5', index=False)
    except ValueError:
        write_log("module can't converge")


if __name__ == '__main__':
    outputFilePath = './data/'

    limit = 8  # rmse upper bound
    main()
    write_log('The End of Execution')


r"""
python D:\StockPrediction\StockPrediction\package\Step_1_ANN_Two.py >> D:\StockPrediction\Log\log_2022-05-15.txt 2>&1
"""
