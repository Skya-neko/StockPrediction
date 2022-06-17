import sys
import pandas as pd


filePath = './data/'
# recordA = sys.argv[1]
# recordB = sys.argv[2]
# target = sys.argv[3]

recordA = 'Step-0_ANNTwoResult_ProcessA.csv'
recordB = 'Step-0_ANNTwoResult_ProcessB.csv'
target = 'Step-0_ANNTwoResult.csv'

recordADF = pd.read_csv(filePath+recordA, index_col=False)
recrodBDF = pd.read_csv(filePath+recordB, index_col=False)
targetDF = pd.read_csv(filePath+target, index_col=False)

recordADF

recordDf = pd.concat([recordADF, recrodBDF], axis=0).reset_index(drop=True)
targetDF = pd.concat([targetDF, recordDf], axis=0).reset_index(drop=True)
targetDF.to_csv(filePath+'test.csv', encoding='big5', index=False)
