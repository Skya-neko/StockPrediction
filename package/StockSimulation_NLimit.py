import math
import numpy as np
import pandas as pd
from datetime import datetime

datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5', index_col=False)
datasetDF = datasetDF[['date', 'open']]

nLimit = 6

# modelFile = 'Step_0_ANN_One_Accuracy.csv'
# modelFile = 'Step_0_MLR_One_Accuracy.csv'
modelFile = 'Step_0_ANN_Two_Accuracy.csv'
predictDF = pd.read_csv(f'./data/{modelFile}', encoding='big5', index_col=False)
predictDF = predictDF[['date', 'close', 'predictedValue']]
# Tick calculate: The tick type in prediction duration only has 1 type: tick = 1
predictDF['predictedValue'] = np.round(predictDF['predictedValue'], 0)

mask = predictDF['date'].isin(['2020-12-30'])
startInd = mask[mask].index.tolist()[0]
mask = predictDF['date'].isin(['2021-12-29'])
endInd = mask[mask].index.tolist()[0]

datasetDF = datasetDF.iloc[startInd:endInd+1].reset_index(drop=True)
predictDF = predictDF.iloc[startInd:endInd+1].reset_index(drop=True)
# predictDF['open'] = datasetDF['open']
predictDF['call'] = None
predictDF['callExpense'] = None
predictDF['put'] = None
predictDF['putExpense'] = None
predictDF['income'] = None


# Income statement
yearDuration = '2021'
income = 0
tradeTimes = 0
tradeExpense = 0
odds = 0
maxLoss = 0
maxProfit = 0
ROI = 0
averageROI = 0
IRR = 0

stockHold = 0

def buy_stock_total_expense(callPrice):
    commissionFee = 0.001425
    expense = callPrice * commissionFee  # A call option gives the holder the right to buy a stock
    expense = math.floor(expense)
    return expense


def sell_stock_total_expense(putPrice):
    commissionFee = 0.001425
    tradeTax = 0.003
    expense = putPrice * (commissionFee + tradeTax)  # a put option gives the holder the right to sell a stock
    expense = math.floor(expense)
    return expense



for i in range(len(predictDF) - 1):
    # Today value
    todayClose = predictDF['close'][i]
    # Tomorrow value
    predictClose = predictDF['predictedValue'][i + 1]
    actualOpen = datasetDF['open'][i + 1]

    predicted_today_spread = predictClose - todayClose  # Spread of close predicted and close today
    if -nLimit <= predicted_today_spread <= nLimit:
        continue

    if stockHold == 0:
        if predicted_today_spread > 0:
            callPrice = actualOpen * 1000
            predictDF['call'][i + 1] = callPrice
            stockHold = 1

            callExpense = buy_stock_total_expense(callPrice)
            predictDF['callExpense'][i + 1] = callExpense
        else:
            pass  # No action
    else:
        if predicted_today_spread > 0:
            pass  # No action
        else:
            putPrice = actualOpen * 1000
            predictDF['put'][i + 1] = putPrice
            stockHold = 0

            putExpense = buy_stock_total_expense(putPrice)
            predictDF['putExpense'][i + 1] = putExpense

            putPrice -= putExpense
            callPrice -= callExpense
            predictDF['income'][i + 1] = putPrice - callPrice

    if i == (len(predictDF) - 2):
        putPrice = actualOpen * 1000
        predictDF['put'][i + 1] = putPrice
        stockHold = 0

        putExpense = buy_stock_total_expense(putPrice)
        predictDF['putExpense'][i + 1] = putExpense

        putPrice -= putExpense
        callPrice -= callExpense
        predictDF['income'][i + 1] = putPrice - callPrice


income = predictDF['income'].sum()
tradeTimes = len(predictDF['put']) - predictDF['put'].isna().sum()
tradeExpense = predictDF['callExpense'].sum() + predictDF['putExpense'].sum()
odds = (predictDF['income'] > 0).sum() / tradeTimes
maxLoss = predictDF['income'].min()
maxProfit = predictDF['income'].max()
ROI = income / predictDF['call'].max()
averageROI = ROI / tradeTimes

print(f'nLimit: {nLimit}')
print(f'income: {income}')
print(f'tradeTimes: {tradeTimes}')
print(f'tradeExpense: {tradeExpense}')
print(f'odds: {odds}')
print(f'maxLoss: {maxLoss}')
print(f'maxProfit: {maxProfit}')
print(f'ROI: {ROI}')
print(f'averageROI: {averageROI}')