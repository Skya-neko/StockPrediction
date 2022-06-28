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

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
# Open CMD window, cd to project root, and execute cmd:
# python   .\package\Step_1_ANN_Two_ModelDFIn.py Step_0_ANN_Two_Result_ProcessC.csv Triple
# And the self-made module can be imported.
# from Step_0_WantedModel import *
# Debug
# from package import Step_1_ANN_Two
from package.Step_0_WantedModel import *



if __name__ == '__main__':
    server = '140.134.25.164'  # DESKTOP-2LNIJAK\MSSQLSERVER
    username = 'Vivian'
    password = 'L102210221022'
    database_name = 'traing_result'
    port = 1433
    conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}'
    engine = create_engine(conn_str)

    # ==================================================================================================================
    # Observed model params
    table = 'ANN_Two_Result'
    limitRMSE = 15
    countDuration = 23  # At least n records satiesfy the limitRMSE
    endureRMSE = 17.7

    observedDF = observed_modelDF(table, limitRMSE, countDuration, endureRMSE)
    i = 0

    paramDict = observedDF.iloc[0].to_dict()
    if paramDict['nesterov'] == 'True':
        paramDict['nesterov'] = True


    # ==================================================================================================================
    # Prepare dataset
    allDatasetDf = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
    mask = allDatasetDf['date'].isin(['2021-01-03'])     # Predict from 2021-01-03
    startIdx = mask[mask].index.tolist()[0] + 10         # Plus 10 make it start from 2021-01-03
    modulo = len(allDatasetDf) % 10

    count = 0  # Set loop stop point
    # Ensure data at last duration be predicted: (len(allDatasetDf) + 10)
    for i_dataset in range(startIdx, len(allDatasetDf) + 10, 10):
        if count >= 1:
            break
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

        count += 1

