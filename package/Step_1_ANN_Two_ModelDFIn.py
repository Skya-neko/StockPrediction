"""
Recursive training model depend on the units of layer.
When find out the observed models, iterate diffrent model parameters except of the units of layer.

"""
import pandas as pd

from package.Step_1_ANN_Two import *
from package.Step_0_WantedModel import *
from datetime import datetime

def check_abandon_units_comb:


if __name__ == '__main__':
    outputFilePath = './data/'
    processRecordFileName = 'Step_0_ANN_Two_Result_ProcessA.csv'  # Debug
    # processRecordFileName = sys.argv[1]
    finalRecordFileName = 'Step_0_ANN_Two_Result.csv'
    limit = 15  # rmse upper bound

    machine = 'Vivian'
    runProcess = 'Single'  # Debug
    # runProcess = sys.argv[2]  # Single, Double, Triple


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

    isAbandoned = check_abandon_units_comb()

    isAbandoned = check_abandon_units_comb()

    seedAmount = 10
    # Use n amount of random seed to train the same units' combination.
    # If these n random seed of specific unit combination still can't  find out best result,
    # then stop to train the specific unit combination in the future.
    for count in range(seedAmount):
        for i in range(len(observedDF)):
            Dense1Units = observedDF['Dense1Units'][i]
            Dense2Units = observedDF['Dense2Units'][i]

            # Model parameters
            randomSeedList = np.random.randint(0, 200, size=1).tolist()
            Dense1List = [Dense1Units]
            Dense2List = [Dense2Units]
            learningRateList = [0.00001, 0.000001]
            decayList = [0, 0.000001, 0.0001, 0.01]
            momentumList = [0.9, 1.2, 0.7]
            epochsList = [2000]
            batchSizeList = [0]

            main()
            write_log('The End of Execution')

    bestDF = best_modelDF(table, limitRMSE=12)
    if not bestDF.empty:
        print('Find the best model!')
        print(bestDF)

    else:
        abandonDF = observedDF['Dense1Units']
        abandonDF['Dense2Units'] = observedDF['Dense2Units']

        # Initialize Step_0_ANN_Two_Abandon.csv
        abandonDF.to_csv('./data/Step_0_ANN_Two_Abandon.csv', encoding='big5', index=False)

        # Step_0_ANN_Two_Abandon.csv append abandon units' comination
        allAbandonDF = pd.read_csv('./data/Step_0_ANN_Two_Abandon.csv', encodings='big5', index_col=False)
        allAbandonDF = pd.concat([allAbandonDF, abandonDF], axis=0).reset_index(drop=True)
        allAbandonDF.to_csv('./data/Step_0_ANN_Two_Abandon.csv', encoding='big5', index=False)

