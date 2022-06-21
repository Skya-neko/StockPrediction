from package.Step_1_ANN_Two import *
from package.Step_0_WantedModel import *
from datetime import datetime


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
    table = 'Step-0_ANN_Two_Result_20220620'
    limitRMSE = 15
    countDuration = 15  # At least n records satiesfy the limitRMSE
    endureRMSE = 50

    observedDF = observed_modelDF(table, limitRMSE, countDuration, endureRMSE)

    observedTime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    # while True:
    for i in range(len(observedDF)):
        # Model parameters
        randomSeedList = np.random.randint(0, 200, size=1).tolist()
        Dense1List = observedDF['Dense1Units'][i]
        Dense2List = observedDF['Dense2Units'][i]
        learningRateList = [0.00001, 0.000001]
        decayList = [0, 0.000001, 0.0001, 0.01]
        momentumList = [0.9, 1.2, 0.7]
        epochsList = [2000]
        batchSizeList = [0]

        main()
        write_log('The End of Execution')