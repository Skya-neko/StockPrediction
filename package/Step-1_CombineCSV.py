import pandas as pd
from datetime import datetime

def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ", something)


filePath = './data/'

recordA = 'Step-0_ANN_Two_Result_ProcessA.csv'
recordB = 'Step-0_ANN_Two_Result_ProcessB.csv'
recordC = 'Step-0_ANN_Two_Result_ProcessC.csv'
recordD = 'Step-0_ANN_Two_Result_ProcessD.csv'
recordE = 'Step-0_ANN_Two_Result_ProcessE.csv'
target = 'Step-0_ANN_Two_Result.csv'

recordADF = pd.read_csv(filePath+recordA, index_col=False)  # ProcessA
recordBDF = pd.read_csv(filePath+recordB, index_col=False)  # ProcessB
recordCDF = pd.read_csv(filePath+recordC, index_col=False)  # ProcessB
recordDDF = pd.read_csv(filePath+recordD, index_col=False)  # ProcessB
recordEDF = pd.read_csv(filePath+recordE, index_col=False)  # ProcessB
targetDF = pd.read_csv(filePath+target, index_col=False)    # Final table



recordDf = pd.concat([recordADF, recordBDF], axis=0)
recordDf = pd.concat([recordDf, recordCDF], axis=0)
recordDf = pd.concat([recordDf, recordDDF], axis=0)
recordDf = pd.concat([recordDf, recordEDF], axis=0)

del recordADF
del recordBDF
del recordCDF
del recordDDF
del recordEDF


compareList = ['startDate', 'endDate', 'random_seed', 'Dense1Units', 'Dense2Units', 'learning_rate', 'decay',
               'momentum', 'nesterov', 'optimizer', 'loss', 'epochs', 'verbose', 'batch_size']

sortList = ['Dense1Units', 'Dense2Units', 'random_seed', 'learning_rate', 'decay',
            'momentum', 'nesterov', 'optimizer', 'loss', 'epochs', 'verbose', 'batch_size', 'startDate', 'endDate']

targetDF = pd.concat([targetDF, recordDf], axis=0)
targetDF = targetDF.drop_duplicates(subset=compareList, keep='last').reset_index(drop=True)
targetDF = targetDF.sort_values(by=sortList).reset_index(drop=True)
targetDF.to_csv(filePath+target, encoding='big5', index=False)


# Initialize the per process record
recordADF = recordADF.head(0)  # Truncate table
recordADF.to_csv(filePath+recordA, encoding='big5', index=False)
recordBDF = recordBDF.head(0)  # Truncate table
recordBDF.to_csv(filePath+recordB, encoding='big5', index=False)
recordCDF = recordCDF.head(0)  # Truncate table
recordCDF.to_csv(filePath+recordC, encoding='big5', index=False)
recordDDF = recordDDF.head(0)  # Truncate table
recordDDF.to_csv(filePath+recordD, encoding='big5', index=False)
recordEDF = recordEDF.head(0)  # Truncate table
recordEDF.to_csv(filePath+recordE, encoding='big5', index=False)
write_log('End')

