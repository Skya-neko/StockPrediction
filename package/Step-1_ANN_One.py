import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time  # 計算function執行時間
from datetime import datetime
import math
import joblib

from tensorflow.compat.v1.keras import Sequential
from tensorflow.compat.v1.keras.layers import Dense
from tensorflow.compat.v1.keras.optimizers import SGD
from tensorflow.compat.v1 import set_random_seed

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

global outputFilePath
global recordFileName

outputFilePath = './data/'
recordFileName = 'Step-0_ANNOneResult.csv'
limit = 8  # 決定rmse最高上限


# Log on terminal
def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ", something)


def CombData(pred):
    # 在前95%的交易日中，設定預測結果和收盤價一致
    sameDays = len(datasetDf) - len(pred)  # 預測結果和收盤價一致的天數
    # 預測結果跟收盤價一致，所以複製DataFrame的close欄數值，並貼上到df新宣告的predictedValue欄
    datasetDf.loc[:, 'predictedValue'] = datasetDf.loc[:, 'close']

    # 在後5%的交易日中，用測試集推算預測股價，用預測的資料蓋掉原後5%的資料
    datasetDf.loc[sameDays:, 'predictedValue'] = pred


def PltCombData():
    pltStart = int(len(datasetDf) * 7 / 10)

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


# 迭代創造新的Dataset，在最後呼叫後續步驟function
def iterateDay():
    # 使用全域變數，讓腳本中的變數統一
    global startDate
    global endDate
    global scaler
    global feature_train_scaled
    global feature_test
    global target_train
    global target_test
    global datasetDf


    datasetDf = pd.read_csv('./data/Step-1_Dataset.csv', encoding='big5')
    mask = datasetDf['date'].isin(['2021-01-03'])
    startIdx = mask[mask].index.tolist()[0]
    startDate = datasetDf["date"][startIdx]
    endDate = datasetDf["date"].iloc[-1]

    write_log(f'{"=" * 20} predict date {startDate} ~ {endDate} {"=" * 20} ')

    # 單獨抓出feature的值，並將其指定給feature。對df使用values函式後，資料型態就會變成ndarray
    new_feature = datasetDf.iloc[:, ~datasetDf.columns.isin(['date',
                                                             'close'])]
    # 劃分特徵值和目標值(都要變成ndarray才可以輸入train_test_split
    new_target = np.array(datasetDf['close'])  # 將df中的'close'欄位，存成numpy的array

    test_size = (len(datasetDf) - startIdx) / len(new_target)
    feature_train, feature_test, target_train, target_test = train_test_split(new_feature, new_target,
                                                                              test_size=test_size,
                                                                              shuffle=False)
    # Save scaler from 2021-01-03~2021-12-29
    # scaler = MinMaxScaler()
    # feature_train_scaled = scaler.fit_transform(feature_train)
    # joblib.dump(scaler, './data/Step-1_Scaler.gz')

    scaler = joblib.load('./data/Step-1_Scaler.gz')
    feature_train_scaled = scaler.fit_transform(feature_train)
    iterate(main)
"""
# Manually Manipulate (Can be use for initialize record file)
def iterate(func):
    paramDict = {
        'random_seed': 200,
        'Dense1Units': 72,
        'Dense2Units': 24,
        'learning_rate': 0.00001,
        'decay': 0,
        'momentum': 0.9,
        'nesterov': True,
        'optimizer': 'sgd',
        'loss': 'mean_squared_error',
        'epochs': 3000,
        'verbose': 0,
        'batch_size': 10,
    }
    func(paramDict)

"""

# """
# 迭代模型每一次的參數
def iterate(func):
    Dense1List = np.random.randint(144, size=10).tolist()
    Dense2List = np.random.randint(144, size=10).tolist()
    lossList = ['mean_squared_error']
    for loss in lossList:
        for random_seed in [200]:
            for Dense1Units in Dense1List:
                for Dense2Units in Dense2List:
                    for learning_rate in [1]:
                        learning_rate = learning_rate / 100000
                        for decay in [0]:
                            decay = decay / 100
                            for momentum in [9]:
                                momentum = momentum / 10
                                for epochs in [2000]:
                                    for batch_size in [10]:
                                        paramDict = {
                                            'random_seed': random_seed,
                                            'Dense1Units': Dense1Units,
                                            'Dense2Units': Dense2Units,
                                            'learning_rate': learning_rate,
                                            'decay': decay,
                                            'momentum': momentum,
                                            'nesterov': True,
                                            'optimizer': 'sgd',
                                            'loss': loss,
                                            'epochs': epochs,
                                            'verbose': 0,
                                            'batch_size': batch_size,
                                        }

                                        # Read data in chuncks to avoid error:
                                        # pandas.errors.ParserError: Error tokenizing data. C error: out of memory
                                        mylist = []
                                        for chunk in pd.read_csv(outputFilePath + recordFileName, sep=',', chunksize=20000):
                                            mylist.append(chunk)
                                        recordDf = pd.concat(mylist, axis=0)
                                        del mylist

                                        ifSameRow = (recordDf[list(paramDict.keys())] == pd.Series(paramDict)).all(1)
                                        if ifSameRow.any():
                                            # 如果比對到已經跑過的資料則Continue
                                            ifLessThan = (recordDf['rmse'][ifSameRow] < limit)

                                        else:
                                            # write_log('SameRow Noooo')
                                            # write_log('New parameters first time.')
                                            # write_log('Input')
                                            # write_log(str(paramDict).replace(', ',',\n').replace("{'","{\n'").replace("}","\n}"))
                                            func(paramDict)

# """
# 訓練模型與儲存資訊
def main(paramDict):
    # write_log('Execute')
    t0 = time.time()
    set_random_seed(paramDict['random_seed'])

    model = Sequential()
    model.add(Dense(units=paramDict['Dense1Units'], activation='relu', input_dim=feature_train_scaled.shape[1], ))
    model.add(Dense(units=paramDict['Dense2Units'], activation='relu', ))
    model.add(Dense(units=1, ))

    sgd = SGD(learning_rate=paramDict['learning_rate'], decay=paramDict['decay'], momentum=paramDict['momentum'],
              nesterov=paramDict['nesterov'])

    model.compile(optimizer=sgd, loss=paramDict['loss'])
    model.fit(feature_train_scaled, target_train, epochs=paramDict['epochs'], verbose=paramDict['verbose'],
              batch_size=paramDict['batch_size'], shuffle=False)

    feature_test_scaled = scaler.transform(feature_test)
    pred = model.predict(feature_test_scaled)

    score = model.evaluate(feature_test_scaled, target_test, verbose=1)
    # write_log(score)
    model.summary()

    CombData(pred)

    # PltCombData()
    try:
        rmse = mean_squared_error(target_test, pred, squared=False)
        # write_log(rmse)
        rmseStr = str(rmse)[:7].replace('.', '_')

        t1 = time.time()

        outputFileName = f'rmseBeyond{limit}'

        # 儲存模型
        if rmse < limit:
            # if not  os.path.exists(outputFilePath):
            #     os.mkdir(outputFilePath)
            outputFileName = 'keras_' + rmseStr + '.h5'
            # model.save(outputFilePath + outputFileName)

        recordDict = {
            'modelName': outputFileName,
            'score': score,
            'rmse': rmse,
            'spendTime': t1 - t0,
            'executionTime(s)': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'startDate': startDate,
            'endDate': endDate,
        }
        write_log('Output')
        write_log(str(recordDict).replace(', ', ',\n').replace("{'", "{\n'").replace("}", "\n}"))
        recordDict.update(paramDict)
        rowDf = pd.DataFrame([recordDict], columns=recordDict.keys())

        # init record file
        # rowDf.to_csv(outputFilePath+recordFileName, encoding='big5', index=False)#init record file
        # recordDf = pd.read_csv(outputFilePath+recordFileName, index_col=False).head(0)  #init record file

        recordDf = pd.read_csv(outputFilePath + recordFileName, index_col=False)
        recordDf = pd.concat([recordDf, rowDf], axis=0).reset_index()
        try:
            recordDf = recordDf.drop(['index'], axis=1)
            recordDf = recordDf.drop(['level_0'], axis=1)
        except KeyError:
            write_log('no level_0 or index column')
        # recordDf = recordDf.drop([0,1,2,3])
        finally:
            recordDf.to_csv(outputFilePath + recordFileName, encoding='big5', index=False)
    except ValueError:
        write_log("module can't converge")

    # 釋放記憶體空間
    del model
    del recordDf

while True:
    iterateDay()
    write_log('The End of Execution')

r"""
python D:\StockPrediction\StockPrediction\package\Step-1_ANN_Two.py >> D:\StockPrediction\Log\log_2022-05-15.txt 2>&1
"""
