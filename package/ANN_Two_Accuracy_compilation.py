import pandas as pd

modelFile = f'Step_0_ANN_Two_Accuracy_{0}.csv'
predictDF = pd.read_csv(f'./data/Step_0_ANN_Two_Accuracy/{modelFile}', encoding='big5', index_col=False)
allPredictDF = predictDF[['date', 'predictedValue']][:-10]

modulo = 1223 % 10
for count in range(25):
    modelFile = f'Step_0_ANN_Two_Accuracy_{count}.csv'
    predictDF = pd.read_csv(f'./data/Step_0_ANN_Two_Accuracy/{modelFile}', encoding='big5', index_col=False)

    if count < 24:
        rowsDF = predictDF[['date', 'predictedValue']][-10:]
        allPredictDF = pd.concat([allPredictDF, rowsDF], axis=0).reset_index(drop=True)
    else:
        rowsDF = predictDF[['date', 'predictedValue']][-modulo:]
        allPredictDF = pd.concat([allPredictDF, rowsDF], axis=0).reset_index(drop=True)
        allPredictDF['close'] = predictDF['close']


allPredictDF.to_csv('./data/Step_0_ANN_Two_Accuracy.csv', encoding='big5', index=False)

