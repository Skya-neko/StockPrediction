import sys
import pandas as pd
from datetime import datetime

def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ", something)


filePath = './data/'
# Receive args from cmd
recordA = sys.argv[1]
recordB = sys.argv[2]
target = sys.argv[3]

# Debug
# recordA = 'Step-0_ANN_Two_Result_ProcessA.csv'
# recordB = 'Step-0_ANN_Two_Result_ProcessB.csv'
# target = 'Step-0_ANN_Two_Result.csv'

recordADF = pd.read_csv(filePath+recordA, index_col=False)  # ProcessA
recordBDF = pd.read_csv(filePath+recordB, index_col=False)  # ProcessB
targetDF = pd.read_csv(filePath+target, index_col=False)    # Final table



recordDf = pd.concat([recordADF, recordBDF], axis=0)
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
write_log('End')

