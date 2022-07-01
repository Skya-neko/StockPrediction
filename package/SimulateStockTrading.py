"""
This stock trading simulation is totally based on trusting the close I predict is totally correct.
Thus rely on the predicted close to buy / sell / hold stock.
"""

import numpy as np
import pandas as pd

datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5', index_col=False)
datasetDF = datasetDF[['date', 'close', 'max', 'min']]

modelFile = 'Step_0_ANN_One_Accuracy.csv'
predictDF = pd.read_csv(f'./data/{modelFile}', encoding='big5', index_col=False)
predictDF = predictDF[['date', 'close', 'predictedValue']]

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
holdStock = 0
# While isHoldWithinADay equal to 0, it means I hold this stock over one day.
# While isHoldWithinADay equal to 1, it means I didn't buy it, or I hold this stock within one day. 
isHoldWithinADay = 1
callPrice = 0
putPrice = 0

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
    # If I'm not holding stock
    if holdStock == 0:
        # I will buy one when I predict I will gain predicted_today_spread.
        if predicted_today_spread > 0:  # Buy
            callPrice = todayClose
            # Wether this trade will success
            if actualMax >= callPrice >= actualMin:
                isHoldWithinADay = 1
                callExpense = buy_stock_total_expense(callPrice)
                holdStock = 1
            else:
                pass
                # Didn't buy anything. Keep holdStock = 0 and isHoldWithinADay = 1
        # If I buy I will at a loss, thus I won't.
        if predicted_today_spread < 0:
            pass  # No action
    # If I'm holding stock
    elif holdStock == 1:
        # And I hold it within one day.
        if isHoldWithinADay == 1:
            if predicted_today_spread > 0:
                pass  # No action
            elif predicted_today_spread < 0:  # Sell
                putPrice = todayClose
                # Wether this trade will success
                if actualMax >= putPrice >= actualMin:
                    isHoldWithinADay = 1
                    putExpense = sell_stock_total_expense(putPrice)
                    holdStock = 0
                else:
                    isHoldWithinADay = 0
        # But I hold it over one day.
        elif isHoldWithinADay == 0:
            # Aim to not lose money! Impossible to sell the stock when knowing that I will be at a loss.
            # tie up happend
            predicted_callPrice_spread = predictClose - callPrice
            if predicted_callPrice_spread > 0:  # Sell
                putPrice = predictClose
                if actualMax >= putPrice >= actualMin:
                    isHoldWithinADay = 1
                    putExpense = sell_stock_total_expense(putPrice)
                    holdStock = 0
                else:
                    isHoldWithinADay = 0
            elif predicted_callPrice_spread < 0:
                pass  # No action
