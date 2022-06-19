import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
from memory_profiler import profile  # Memory Observation
import itertools
from multiprocessing import Process, Queue



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


def PltCombData(datasetDf):
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

def check_wether_trained_params(filePath, checkTagetName, paramDict, startDate, endDate):
    trained = False
    recordDf = pd.read_csv(filePath + checkTagetName, index_col=False)

    # Check wether the model parameters have been trained before
    ifSameRow = (recordDf[list(paramDict.keys())] == pd.Series(paramDict)).all(1)
    if ifSameRow.any():
        # Check wether all the rmse of traind parameter is smaller than limitation
        ifLessThan = (recordDf['rmse'][ifSameRow] < limit)
        if ifLessThan.all():
            mask1 = recordDf[['startDate', 'endDate']].loc[ifLessThan.index]
            mask2 = pd.Series({'startDate': startDate, 'endDate': endDate})
            # Check wether the duration has been trained
            ifSameDate = (mask1 == mask2).all(1)
            if ifSameDate.any():
                trained = 'continue'   # Train other new duration!
        else:
            # Break the dutations loop to avoid to waste time on check the same params in all durations
            trained = 'break'
    return trained

def train_model(paramDict, feature_train_scaled, feature_test_scaled, target_train, target_test, queue):
    from tensorflow.compat.v1.keras import Sequential
    from tensorflow.compat.v1.keras.layers import Dense
    from tensorflow.compat.v1.keras.optimizers import SGD
    from tensorflow.compat.v1 import set_random_seed

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

    stringlist = []
    model.summary(print_fn=lambda x: stringlist.append(x))
    short_model_summary = "\n".join(stringlist)

    queue.put(pred)
    queue.put(score)
    queue.put(short_model_summary)
    queue.put(t0)


# @profile   # uncomment for memory obervation & don't use in debugger mode
def main():
    # Model parameters
    randomSeedList = [200]
    Dense1List = np.random.randint(4, 144, size=1).tolist()
    Dense2List = np.random.randint(4, 256, size=1).tolist()
    learningRateList = [0.00001]
    decayList = [0]
    momentumList = [0.9]
    epochsList = [2000]
    batchSizeList = [10]

    # Generate iterator for every combination of elements in lists
    paramIterator = itertools.product(randomSeedList, Dense1List, Dense2List, learningRateList,
                                      decayList, momentumList, epochsList, batchSizeList)

    for i_param in paramIterator:
        paramDict = new_param_dict(*i_param)

        allDatasetDf = pd.read_csv('./data/Step-1_Dataset.csv', encoding='big5')
        mask = allDatasetDf['date'].isin(['2021-01-03'])     # Predict from 2021-01-03
        startIdx = mask[mask].index.tolist()[0] + 10         # Plus 10 make it start from 2021-01-03

        # Ensure data at last duration be predicted: (len(allDatasetDf) + 10)
        for i_dataset in range(startIdx, len(allDatasetDf) + 10, 10):
            # Ensure data at last duration be predicted
            if i_dataset > len(allDatasetDf):
                i_dataset = len(allDatasetDf) - 1

            datasetDf = allDatasetDf.loc[:i_dataset, ]
            startDate = datasetDf["date"][i_dataset - 10]    # Predict from this date at this time
            endDate = datasetDf["date"][i_dataset]           # Predict from this date at this time

            write_log(f'{"=" * 20} predict date {startDate} ~ {endDate} {"=" * 20} ')

            # Select all rows, all columns except date and close as feature
            new_feature = datasetDf.iloc[:, ~datasetDf.columns.isin(['date', 'close'])]
            # Select close price as target
            # "Func: train_test_split" must input DataFrame or numpy array,
            # Turn pd.Series into np.array.
            new_target = np.array(datasetDf['close'])

            test_size = 10 / len(new_target)                 # Split last 10 days into test dataset
            feature_train, feature_test, target_train, target_test = train_test_split(new_feature, new_target,
                                                                                      test_size=test_size,
                                                                                      shuffle=False)

            scaler = MinMaxScaler()
            feature_train_scaled = scaler.fit_transform(feature_train)
            feature_test_scaled = scaler.transform(feature_test)


            # """ # Comment this snippet for initializing result file

            # Check final result data
            trained = check_wether_trained_params(outputFilePath, finalRecordFileName, paramDict, startDate, endDate)
            # If trained == False, then program keep going.
            if trained == 'continue':
                continue
            elif trained == 'break':
                break
            
            if finalRecordFileName != processRecordFileName:
                # Check process result data
                trained = check_wether_trained_params(outputFilePath, processRecordFileName, paramDict, startDate, endDate)
                # If trained == False, then program keep going.
                if trained == 'continue':
                    continue
                elif trained == 'break':
                    break

            # """ # Comment this snippet for initializing result file

            queue = Queue()
            model_process = Process(target=train_model,
                                    args=(paramDict, feature_train_scaled, feature_test_scaled,
                                          target_train, target_test, queue))
            model_process.start()
            model_process.join()   # Continue the main process after execution of child process

            pred = queue.get()
            score = queue.get()
            short_model_summary = queue.get()
            t0 = queue.get()

            print(short_model_summary)


            # Visualize result
            # CombData(datasetDf, pred)
            # PltCombData(datasetDf)


            # Save result
            try:
                rmse = mean_squared_error(target_test, pred, squared=False)
                # write_log(rmse)
                rmseStr = str(rmse)[:7].replace('.', '_')

                t1 = time.time()

                outputFileName = f'rmseBeyond{limit}'

                if rmse < limit:
                    outputFileName = 'keras_' + rmseStr + '.h5'

                recordDict = {
                    'modelName': outputFileName,
                    'score': f'{score:.2f}',
                    'rmse': f'{rmse:.2f}',
                    'spendTime': f'{t1 - t0:.2f}',
                    'executionTime': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    'startDate': startDate,
                    'endDate': endDate,
                    'machine': machine,
                    'runProcess': runProcess,

                }
                write_log('Output')
                write_log(str(recordDict).replace(', ', ',\n').replace("{'", "{\n'").replace("}", "\n}"))
                recordDict.update(paramDict)
                rowDf = pd.DataFrame([recordDict], columns=recordDict.keys())

                # Initialize record file
                # rowDf.to_csv(outputFilePath+processRecordFileName, encoding='big5', index=False)
                # recordDf = pd.read_csv(outputFilePath+processRecordFileName, index_col=False).head(0)

                recordDf = pd.read_csv(outputFilePath + processRecordFileName, index_col=False)
                recordDf = pd.concat([recordDf, rowDf], axis=0).reset_index(drop=True)
                recordDf.to_csv(outputFilePath + processRecordFileName, encoding='big5', index=False)
            except ValueError:
                write_log("module can't converge")


if __name__ == '__main__':
    outputFilePath = './data/'
    processRecordFileName = sys.argv[1]
    # processRecordFileName = 'Step-0_ANN_Two_Result_ProcessA.csv'  # Debug
    finalRecordFileName = 'Step-0_ANN_Two_Result.csv'
    limit = 8  # rmse upper bound

    machine = 'Vivian'
    runProcess = sys.argv[2]  # Single, Double, Triple
    while True:
        main()
        write_log('The End of Execution')

r"""
python D:\StockPrediction\StockPrediction\package\Step-1_ANN_Two.py >> D:\StockPrediction\Log\log_2022-05-15.txt 2>&1
"""
