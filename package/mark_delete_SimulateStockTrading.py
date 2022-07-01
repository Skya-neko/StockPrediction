"""
This stock trading simulation is totally based on trusting the close I predict is totally correct.
Thus rely on the predicted close to buy / sell / hold stock.
"""

import numpy as np
import pandas as pd
from datetime import datetime

datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5', index_col=False)
datasetDF = datasetDF[['date', 'close', 'max', 'min']]

modelFile = 'Step_0_ANN_One_Accuracy.csv'
predictDF = pd.read_csv(f'./data/{modelFile}', encoding='big5', index_col=False)
predictDF = predictDF[['date', 'close', 'predictedValue']]

startInd = predictDF['date'].isin(['2020-12-30']).index.tolist()[0]
endInd = predictDF['date'].isin(['2020-12-30']).index.tolist()[0]

datasetDF = datasetDF.iloc[startInd:endInd]
predictDF = predictDF.iloc[startInd:endInd]


# Income statement
investRule = 'Day-trading'
yearDuration = '2021'
income = 0
callTimes = 0
putTimes = 0
callSuccessRate = 0
putSuccessRate = 0
tradeExpense = 0
odds = 0
maxLoss = 0
maxProfit = 0
ROI = 0
averageROI = 0
IRR = 0

# Initial
callPrice = 0
putPrice = 0


# holdStock = 0, isWithinADay = 1 ==> Don't have anything: I can't buy / I don't take action / I sell it.
# holdStock = 0, isWithinADay = 0 ==> I can't buy / I don't take action over one day.
# holdStock = 1, isWithinADay = 1 ==> I buy it tomorrow
# holdStock = 1, isWithinADay = 0 ==> I can't sell it.
holdStock = 0
isWithinADay = 1


# Tick calculate: The tick type in prediction duration only has 1 type: tick = 1
predictDF['predictedValue'] = np.round(predictDF['predictedValue'], 0)
print(predictDF)


def buy_stock_total_expense(callPrice):
    commissionFee = 0.001425
    expense = callPrice * commissionFee  # A call option gives the holder the right to buy a stock
    return expense


def sell_stock_total_expense(putPrice):
    commissionFee = 0.001425
    tradeTax = 0.003
    expense = putPrice * (commissionFee + tradeTax)  # a put option gives the holder the right to sell a stock
    return expense


# tradeExpense = buy_stock_total_expense(callPrice) + sell_stock_total_expense(putPrice)

for i in range(len(predictDF) - 1):
    # Today value
    todayClose = predictDF['close'][i]
    # Tomorrow value
    predictClose = predictDF['predictedValue'][i + 1]
    actualClose = predictDF['close'][i + 1]
    actualMax = datasetDF['max'][i + 1]
    actualMin = datasetDF['min'][i + 1]

    predicted_today_spread = predictClose - todayClose  # Spread of close predicted and close today


    # This snippet check my condition now: wether I hold stock?
    # If I'm not holding stock
    if holdStock == 0:
        if predicted_today_spread > 0:
            callPrice = todayClose
            if actualMax >= callPrice >= actualMin:
                # Buy it tomorrow
                callExpense = buy_stock_total_expense(callPrice)
                holdStock = 1
                isWithinADay = 1
            else:
                # I can't buy
                holdStock = 0
                isWithinADay = 0
        elif predicted_today_spread < 0:
            # No action: I can't earn money
            holdStock = 0
            isWithinADay = 0
    # If I'm holding stock over one day
    elif holdStock == 1 and isWithinADay == 0:
        # Aim to not lose money! Impossible to sell the stock when knowing that I will be at a loss.
        # tie up happend
        predicted_callPrice_spread = predictClose - callPrice
        if predicted_callPrice_spread > 0:
            putPrice = predictClose
            if actualMax >= putPrice >= actualMin:
                # I sell it some day.
                putExpense = sell_stock_total_expense(putPrice)
                holdStock = 0
                isWithinADay = 1
            else:
                # I can't sell it.
                holdStock == 1
                isWithinADay = 0
        elif predicted_callPrice_spread < 0:
            # No action: I can't earn money
            holdStock == 1
            isWithinADay = 0




    if holdStock == 1 and isWithinADay == 1:
        putPrice = predictClose
        if actualMax >= putPrice >= actualMin:
            # Buy it and sell it tomorrow.
            putExpense = sell_stock_total_expense(putPrice)
            holdStock = 0
            isWithinADay = 1
        else:
            # I can't sell it.
            holdStock = 1
            isWithinADay = 0
