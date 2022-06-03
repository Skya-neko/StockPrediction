# -*- coding: utf-8 -*-


import os 
rootDirect = 'C:/Users/Vivian/Desktop/資訊碩士/資訊碩二上/畢業論文研究/StockPrediction'
NTUSD = 'data/Sentimental Feature/Text-mining-exercise-main/Text-mining-exercise-main/'
selfDict = 'data/Sentimental Feature/self_taiwan_stock_terms/'
aggregateDict = 'data/Sentimental Feature/aggregation_dictionary/'
os.chdir(rootDirect)

with open(NTUSD+'Step-4_NTUSDNegative.txt',mode = 'r',encoding= 'utf-16') as file:
    NTUSD_n = file.read().split('\n')
    
with open(NTUSD+'Step-4_NTUSDPositive.txt',mode = 'r',encoding= 'utf-16') as file:
    NTUSD_p = file.read().split('\n')
    
with open(selfDict+'Step-4_SelfNegative.txt',mode = 'r',encoding= 'utf-8') as file:
    selfDict_n = file.read().split('\n')
    
with open(selfDict+'Step-4_SelfPositive.txt',mode = 'r',encoding= 'utf-8') as file:
    selfDict_p = file.read().split('\n')
    
all_n = NTUSD_n.copy()
all_p = NTUSD_p.copy()

for i in selfDict_n:
    if i not in all_n:
        all_n.append(i)

for i in selfDict_p:
    if i not in all_p:
        all_p.append(i)


all_n.remove('')
all_p.remove('')



with open(aggregateDict+'Step-4_SelfNegative.txt',mode = 'w',encoding= 'utf-8') as file:
    for i in all_n:
        file.write('{}\n'.format(i))

    
with open(aggregateDict+'Step-4_SelfPositive.txt',mode = 'w',encoding= 'utf-8') as file:
    for i in all_p:
        file.write('{}\n'.format(i))
