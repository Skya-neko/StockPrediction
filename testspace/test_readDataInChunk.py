import pandas as pd
mylist = []
for chunk in pd.read_csv('data/Step-0_ANNTwoResult.csv', sep=',', chunksize=20000):
    mylist.append(chunk)
recordDf = pd.concat(mylist, axis=0)
del mylist