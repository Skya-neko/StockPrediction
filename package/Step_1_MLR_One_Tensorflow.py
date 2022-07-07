# =============================================================================
# import module
# =============================================================================
#資料分析套件
import time
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from sklearn.model_selection import train_test_split



import tensorflow as tf
# from tensorflow import set_random_seed  # Wrong code
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Normalization
from tensorflow.keras.optimizers import SGD

from sklearn.preprocessing import MinMaxScaler

#sklearn MLP
from sklearn.metrics import mean_squared_error


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
    plt.savefig('Step_0_MLR_One_Result_Tensorflow.png')
    plt.close()
    # plt.show()


def new_param_dict(random_seed, Dense1Units,
                   Dense2Units, learning_rate,
                   decay, momentum,
                   epochs, batch_size):
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
def main(paramDict):
    datasetDf = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
    mask = datasetDf['date'].isin(['2021-01-03'])  # Predict from 2021-01-03
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



    t0 = time.time()
    tf.random.set_seed(paramDict['random_seed'])
    # multiple inputs
    linear_model = tf.keras.Sequential([
        normalizer,
        layers.Dense(units=1)  # Linear Model
    ])

    linear_model.layers[1].kernel
    sgd = SGD(learning_rate=paramDict['learning_rate'], decay=paramDict['decay'],
              momentum=paramDict['momentum'], nesterov=paramDict['nesterov'])

    linear_model.compile(
        # optimizer=tf.keras.optimizers.Adam(learning_rate=paramDict['learning_rate']),
        optimizer=sgd,
        loss=paramDict['loss'])
    history = linear_model.fit(
        feature_train,
        target_train,
        epochs=paramDict['epochs'],
        # Suppress logging.
        verbose=paramDict['verbose'],
        # Calculate validation results on 20% of the training data.
        validation_split=0.2)
    # plot_loss(history)
    print('yes')



    pred = linear_model.predict(feature_test)
    score = linear_model.evaluate(feature_test, target_test, verbose=1)
    linear_model.summary()

    CombData(datasetDf, pred)
    PltCombData(datasetDf)

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
        write_log('Output')
        write_log(str(recordDict).replace(', ', ',\n').replace("{'", "{\n'").replace("}", "\n}"))
        recordDict.update(paramDict)
        rowDf = pd.DataFrame([recordDict], columns=recordDict.keys())
        #
        # # Initialize record file
        # # rowDf.to_csv(outputFilePath+recordFileName, encoding='big5', index=False)
        # # recordDf = pd.read_csv(outputFilePath+recordFileName, index_col=False).head(0)
        #
        recordDf = pd.read_csv(outputFilePath + recordFileName, index_col=False)
        recordDf = pd.concat([recordDf, rowDf], axis=0).reset_index(drop=True)
        recordDf.to_csv(outputFilePath + recordFileName, encoding='big5', index=False)
    except ValueError:
        write_log("module can't converge")


if __name__ == '__main__':
    outputFilePath = './data/'
    recordFileName = 'Step_0_MLR_One_Result.csv'
    recordCheckFileName = 'Step_0_MLR_One_Result.csv'
    limit = 8  # rmse upper bound
    while True:
        # Model parameters
        randomSeedList = np.random.randint(4, 200, size=1).tolist()
        Dense1List = [None]
        Dense2List = [None]
        learningRateList = [0.001, 0.0001, 0.00001, 0.000001, 0.0000001]
        decayList = [0, 0.01, 0.001, 0.0001]
        momentumList = [0.9]
        epochsList = [2000, 4000]
        batchSizeList = [0]


        # Generate iterator for every combination of elements in lists
        paramIterator = itertools.product(randomSeedList, Dense1List, Dense2List, learningRateList,
                                          decayList, momentumList, epochsList, batchSizeList)

        for i_param in paramIterator:
            paramDict = new_param_dict(*i_param)

            # # """ # Comment this snippet for initialize result file
            #
            # # Read data in chuncks to avoid error:
            # # pandas.errors.ParserError: Error tokenizing data. C error: out of memory
            # mylist = []
            # for chunk in pd.read_csv(outputFilePath + recordCheckFileName, sep=',', chunksize=20000):
            #     mylist.append(chunk)
            # recordDf = pd.concat(mylist, axis=0)
            # del mylist
            #
            # # Check wether the model parameters have been trained before
            # ifSameRow = (recordDf[list(paramDict.keys())] == pd.Series(paramDict)).all(1)
            # if ifSameRow.any():
            #     # Check wether all the rmse of traind parameter is smaller than limitation
            #     ifLessThan = (recordDf['rmse'][ifSameRow] < limit)
            #     if ifLessThan.all():
            #         mask1 = recordDf[['startDate', 'endDate']].loc[ifLessThan.index]
            #         mask2 = pd.Series({'startDate': startDate, 'endDate': endDate})
            #         # Check wether the duration has been trained
            #         ifSameDate = (mask1 == mask2).all(1)
            #         if ifSameDate.any():
            #             continue
            #     else:
            #         break
            #
            # # """ # Comment this snippet for initialize result file

            main(paramDict)
            write_log('The End of Execution')
