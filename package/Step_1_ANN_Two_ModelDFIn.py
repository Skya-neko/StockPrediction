"""
Recursive training model depend on the units of layer.
When find out the observed models, iterate diffrent model parameters except of the units of layer.

"""
import sys
import pandas as pd
import numpy as np
from datetime import datetime
# Open CMD window, cd to project root, and execute cmd:
# python   .\package\Step_1_ANN_Two_ModelDFIn.py Step_0_ANN_Two_Result_ProcessC.csv Triple
# And the self-made module can be imported.
import Step_1_ANN_Two
from Step_0_WantedModel import *


def check_whether_abandon_units(outputFilePath, recordFileName, Dense1Units, Dense2Units):
    recordDF = pd.read_csv(outputFilePath+recordFileName, index_col=False)
    unitsComb = pd.Series({'Dense1Units': Dense1Units, 'Dense2Units': Dense2Units})
    mask = (recordDF[['Dense1Units', 'Dense2Units']] == unitsComb)
    compareList = ['random_seed', 'Dense1Units', 'Dense2Units']
    candidateDF = recordDF[mask]
    # Find out the count of different random_seed from data under the same combination of units.
    candidateDF = candidateDF.drop_duplicates(subset=compareList, keep='last').reset_index(drop=True)
    count = len(candidateDF)
    if count > seedCount:
        return True
    else:
        return False






if __name__ == '__main__':
    outputFilePath = './data/'
    # processRecordFileName = 'Step_0_ANN_Two_Result_ProcessA.csv'  # Debug
    processRecordFileName = sys.argv[1]
    finalRecordFileName = 'Step_0_ANN_Two_Result.csv'
    limit = 15  # rmse upper bound

    machine = 'Vivian'
    # runProcess = 'Single'  # Debug
    runProcess = sys.argv[2]  # Single, Double, Triple


    # Observed model params
    # Find out the condition that there are n_countDuration records satisfied the limit n_limitRMSE per model,
    # And all rmse at all duration in a model should smaller than n_endureRMSE
    table = 'Step-0_ANN_Two_Result_20220620'
    limitRMSE = 15
    countDuration = 15  # At least n records satiesfy the limitRMSE
    endureRMSE = 50

    observedDF = observed_modelDF(table, limitRMSE, countDuration, endureRMSE)

    observedTime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    observedLogDF = pd.DataFrame({'limitRMSE':[limitRMSE],
                                  'countDuration': [countDuration],
                                  'endureRMSE': [endureRMSE],
                                  'observedTime': [observedTime],
                                  })
    observedLogDF.to_csv('./data/Step_0_ANN_Two_ObservedLog.csv', encoding='big5', index=False)

    seedCount = 10
    # Use n amount of random seed to train the same combination of units.
    # If these n random seed of specific unit combination still can't  find out best result,
    # then stop to train the specific unit combination in the future.
    for count in range(seedCount):
        for i in range(len(observedDF)):
            Dense1Units = observedDF['Dense1Units'][i]
            Dense2Units = observedDF['Dense2Units'][i]

            isAbandoned = check_whether_abandon_units(outputFilePath, finalRecordFileName, Dense1Units, Dense2Units)
            if isAbandoned:
                break
            isAbandoned = check_whether_abandon_units(outputFilePath, processRecordFileName,Dense1Units, Dense2Units)
            if isAbandoned:
                break

            # Model parameters
            randomSeedList = np.random.randint(0, 200, size=1).tolist()
            Dense1List = [Dense1Units]
            Dense2List = [Dense2Units]
            learningRateList = [0.00001, 0.000001]
            decayList = [0, 0.000001, 0.0001, 0.01]
            momentumList = [0.9, 1, 0.7]
            epochsList = [2000]
            batchSizeList = [0]

            Step_1_ANN_Two.main(randomSeedList, Dense1List, Dense2List, learningRateList,
                                decayList, momentumList, epochsList, batchSizeList,
                                outputFilePath, processRecordFileName, finalRecordFileName, limit,
                                machine, runProcess)
            Step_1_ANN_Two.write_log('The End of Execution')

    bestDF = best_modelDF(table, limitRMSE=12)
    if not bestDF.empty:
        print('Find the best model!')
        print(bestDF)

