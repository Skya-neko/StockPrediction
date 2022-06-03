# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 17:02:52 2021

@author: Vivian
"""

import numpy as np
import pandas as pd
from FinMind import strategies
from FinMind.data import DataLoader
from FinMind.strategies.base import Strategy
from ta.momentum import StochasticOscillator


data_loader = DataLoader()
# data_loader.login(user_id, password) # 可選
obj = strategies.BackTest(
     stock_id="2330",
     start_date="2017-01-01",
     end_date="2021-01-01",
     trader_fund=500000.0,
     fee=0.001425,
     data_loader=data_loader,
)
stock0056 =  obj.stock_price
del(stock0056['CashEarningsDistribution'])
del(stock0056['StockEarningsDistribution'])
stock0056.to_csv('data/Step-2_StockPrice.csv')

