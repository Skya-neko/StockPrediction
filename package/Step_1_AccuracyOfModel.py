# # Case 1:
# closeSpread + predict +
# closeSpread - predict -



import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sklearn.metrics import mean_squared_error

# accuracyFile = './data/Step_0_ANN_One_Accuracy.csv'
accuracyFile = './data/Step_0_ANN_Two_Accuracy.csv'
datasetDF = pd.read_csv(accuracyFile, encoding='big5', index_col=False)
mask = datasetDF['date'].isin(['2021-01-03'])     # Predict from 2021-01-03
startIdx = mask[mask].index.tolist()[0]

# =======
# rmse
target_test = datasetDF['close'][startIdx:]
pred = datasetDF['predictedValue'][startIdx:]
rmse = mean_squared_error(target_test, pred, squared=False)
# =======



startDate = datasetDF["date"][startIdx]
endDate = datasetDF["date"].iloc[-1]


latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
closeSpread = latter - former
closeFirstDay = 183 - 181.5
closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)


latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
former = datasetDF['predictedValue'].iloc[:-1].reset_index(drop=True)
predictedValueSpread = latter - former
closeFirstDay = 183 - 181.5
predictedValueSpread = pd.concat([pd.Series([closeFirstDay]), predictedValueSpread], axis=0).reset_index(drop=True)

closeSpread = closeSpread[startIdx:].reset_index(drop=True)
predictedValueSpread = predictedValueSpread[startIdx:].reset_index(drop=True)

TP = 0
TN = 0
FP = 0
FN = 0
# T: Correctly recognize the sample
# F: Uncorrectly recognize the sample
# P: the sample belongs to A category (stock price rise)
# N: the sample belongs to B category (stock price fall)



for i in range(len(closeSpread)):
    # Stock price rise
    if closeSpread[i] >= 0:
        if predictedValueSpread[i] >= 0:
            TP += 1
        else:
            FP += 1
    # Stock price fall
    else:
        if predictedValueSpread[i] < 0:
            TN += 1
        else:
            FN += 1

accuracy = (TP+TN) / (TP+TN+FP+FN)
precision = TP / (TP+FP)
recall = TP / (TP+FN)
recallNegative = TN / (TN+FP)  # recall of negative sample
f1 = 2 * precision * recall / (precision+recall)
