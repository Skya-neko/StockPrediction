# # Case 1:
# closeSpread + score +
# closeSpread - score -


import pandas as pd

datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
datasetDF = datasetDF[['date', 'close', 'Score']]
latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
closeSpread = latter - former
closeFirstDay = 183 - 181.5
closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)

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
        if datasetDF['Score'][i] >= 0:
            TP += 1
        else:
            FP += 1
    # Stock price fall
    else:
        if datasetDF['Score'][i] < 0:
            TN += 1
        else:
            FN += 1

accuracy = (TP+TN) / (TP+TN+FP+FN)
precision = TP / (TP+FP)
recall = TP / (TP+FN)
f1 = 2 * precision * recall / (precision+recall)

# ======================================================================================================================
# Case 2:
# closeSpread 0~0.05  score 0~0.5
# closeSpread 0.05~0.1  score 0.5~1
# closeSpread 0~-0.05  score 0~-0.5
# closeSpread -0.05~-0.1  score -0.5~-1

# import pandas as pd
#
# datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
# datasetDF = datasetDF[['date', 'close', 'Score']]
# latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
# former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
# closeSpread = latter - former
# closeFirstDay = 183 - 181.5
# closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)
#
# scoreMon = max(datasetDF['Score']) - min(datasetDF['Score'])
# scoreScaled = (datasetDF['Score'] - min(datasetDF['Score'])) / scoreMon
# scoreScaled = scoreScaled - 0.5  # Make the value of element in the middel 0
#
#
# amplitudeDaily = closeSpread/datasetDF['close']
#
#
# # Stock rise
# amplitudePart = 0.05
# scorePart = 0.25
# for j in range(2):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(amplitudeDaily)):
#         # Inside the bounds
#         if (j * amplitudePart) < amplitudeDaily[i] <= ((j + 1) * amplitudePart):
#             count += 1
#             if (j*scorePart) > scoreScaled[i] and scoreScaled[i] <= ((j+1)*scorePart):
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if not (j*scorePart) > scoreScaled[i] and scoreScaled[i] <= ((j+1)*scorePart):
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} accuracy:', count)
#
#
#
# # Stock fall
# amplitudePart = -0.05
# scorePart = -0.25
# for j in range(2):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(amplitudeDaily)):
#         # Inside the bounds
#         if (j * amplitudePart) >= amplitudeDaily[i] >= ((j + 1) * amplitudePart):
#             count += 1
#             if (j * scorePart) >= scoreScaled[i] >= ((j + 1) * scorePart):
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if not (j * scorePart) >= scoreScaled[i] >= ((j + 1) * scorePart):
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} accuracy:', count)

# ======================================================================================================================
# # Case 3:
# # closeSpread 0~0.05  score +
# # closeSpread 0.05~0.1  score +
# # closeSpread 0~-0.05  score -
# # closeSpread -0.05~-0.1  score -
#
# import pandas as pd
#
# datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
# datasetDF = datasetDF[['date', 'close', 'Score']]
# latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
# former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
# closeSpread = latter - former
# closeFirstDay = 183 - 181.5
# closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)
#
# scoreMon = max(datasetDF['Score']) - min(datasetDF['Score'])
# scoreScaled = (datasetDF['Score'] - min(datasetDF['Score'])) / scoreMon
# scoreScaled = scoreScaled - 0.5  # Make the value of element in the middel 0
#
#
# amplitudeDaily = closeSpread/datasetDF['close']
#
# # Stock rise
# amplitudePart = 0.05
# for j in range(2):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(amplitudeDaily)):
#         # Inside the bounds
#         if (j * amplitudePart) < amplitudeDaily[i] <= ((j + 1) * amplitudePart):
#             count += 1
#             # print(f'{j*amplitudePart} < this, this <= {(j+1)*amplitudePart}')
#             # print(amplitudeDaily[i])
#             if scoreScaled[i] >= 0:
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if scoreScaled[i] < 0:
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} accuracy:', count)
#
#
#
# # Stock fall
# amplitudePart = -0.05
# for j in range(2):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(amplitudeDaily)):
#         # Inside the bounds
#         if (j * amplitudePart) >= amplitudeDaily[i] >= ((j + 1) * amplitudePart):
#             count += 1
#             if scoreScaled[i] >= 0:
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if scoreScaled[i] < 0:
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} accuracy:', count)


# ======================================================================================================================
# # Case 4:
# # closeSpread      0  ~  0.02   score +
# # closeSpread   0.02  ~  0.04   score +
# # closeSpread   0.04  ~  0.06   score +
# # closeSpread   0.06  ~  0.08   score +
# # closeSpread   0.08  ~  0.1    score +
# # closeSpread      0  ~ -0.02   score -
# # closeSpread  -0.02  ~ -0.04   score -
# # closeSpread  -0.04  ~ -0.06   score -
# # closeSpread  -0.06  ~ -0.08   score -
# # closeSpread  -0.08  ~ -0.1    score -
# # The logic of this assumption is wrong, because we use score to predict price.
# # But under this assumption, it use spread to check performance of score.
#
#
#
# import pandas as pd
#
# datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
# datasetDF = datasetDF[['date', 'close', 'Score']]
# latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
# former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
# closeSpread = latter - former
# closeFirstDay = 183 - 181.5
# closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)
#
# scoreMon = max(datasetDF['Score']) - min(datasetDF['Score'])
# scoreScaled = (datasetDF['Score'] - min(datasetDF['Score'])) / scoreMon
# scoreScaled = scoreScaled - 0.5  # Make the value of element in the middel 0
#
#
# amplitudeDaily = closeSpread/datasetDF['close']
#
# # Stock rise
# amplitudePart = 0.02
# for j in range(5):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(amplitudeDaily)):
#         # Inside the bounds
#         if (j * amplitudePart) < amplitudeDaily[i] <= ((j + 1) * amplitudePart):
#             count += 1
#             # print(f'{j*amplitudePart} < this, this <= {(j+1)*amplitudePart}')
#             # print(amplitudeDaily[i])
#             if scoreScaled[i] >= 0:
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if scoreScaled[i] < 0:
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} count:', count)
#
#
#
# # Stock fall
# amplitudePart = -0.02
# for j in range(5):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(amplitudeDaily)):
#         # Inside the bounds
#         if (j * amplitudePart) >= amplitudeDaily[i] >= ((j + 1) * amplitudePart):
#             count += 1
#             if scoreScaled[i] >= 0:
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if scoreScaled[i] < 0:
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} count:', count)


# ======================================================================================================================
# # Case 5:
# # closeSpread and score are all between 1 ~ -1
# # score: rate of score spread use sklearn standard scale
# # closeSpread: rate of price spread divide by price limite
# # Fail because divide 0 happend in score calculation
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
#
#
#
# datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
# datasetDF = datasetDF[['date', 'close', 'Score']]
#
# latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
# former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
# closeSpread = latter - former
# closeFirstDay = 183 - 181.5
# closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)
#
# closeSpreadRate = closeSpread/datasetDF['close']  # Rate of price spread
# # Normalize into 1 ~ -1: Rate of price spread divide by price limit
# # price limit in Taiwan = 0.10
# closeSpreadRateScaled = closeSpreadRate / 0.10
#
#
# latter = datasetDF['Score'].iloc[1:].reset_index(drop=True)
# former = datasetDF['Score'].iloc[:-1].reset_index(drop=True)
# scoreSpread = latter - former
# scoreFirstDay = 24 - 27  # 27 from rerun Step-3_SentimentScore
# scoreSpread = pd.concat([pd.Series([scoreFirstDay]), scoreSpread], axis=0).reset_index(drop=True)
#
# scoreSpreadRate = scoreSpread/datasetDF['Score']  # Rate of price spread
# print(scoreSpread[83])
# print(datasetDF['Score'][83])
# # Normalize into 1 ~ -1: use sklearn standard scale
# scaler = StandardScaler()
# scoreSpreadRate = np.asarray(scoreSpreadRate)
# scoreSpreadRate = scoreSpreadRate.reshape(-1,1)
# scaler.fit(scoreSpreadRate)
# scoreSpreadRateScaled = scaler.transform(scoreSpreadRate)
#
# # Stock rise
# spreadPart = 0.5
# for j in range(2):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(closeSpreadRateScaled)):
#         # Inside the bounds
#         if (j * spreadPart) < closeSpreadRateScaled[i] <= ((j + 1) * spreadPart):
#             count += 1
#             # print(f'{j*spreadPart} < this, this <= {(j+1)*spreadPart}')
#             # print(amplitudeDaily[i])
#             if (j * spreadPart) < scoreSpreadRateScaled[i] <= ((j + 1) * spreadPart):
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if (j * spreadPart) >= scoreSpreadRateScaled[i] and scoreSpreadRateScaled[i] > ((j + 1) * spreadPart):
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} accuracy:', count)
#
#
#
# # Stock fall
# spreadPart = -0.5
# for j in range(2):
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     count = 0
#     for i in range(len(closeSpreadRateScaled)):
#         # Inside the bounds
#         if (j * spreadPart) >= closeSpreadRateScaled[i] >= ((j + 1) * spreadPart):
#             count += 1
#             if (j * spreadPart) >= scoreSpreadRateScaled[i] >= ((j + 1) * spreadPart):
#                 TP += 1
#             else:
#                 FP += 1
#         # outside the bounds
#         else:
#             if (j * spreadPart) < scoreSpreadRateScaled[i] and scoreSpreadRateScaled[i] < ((j + 1) * spreadPart):
#                 TN += 1
#             else:
#                 FN += 1
#         # print('TP', TP)
#         # print('FP', FP)
#         # print('TN', TN)
#         # print('FN', FN)
#
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     print(f'part {j} accuracy:', accuracy)
#     print(f'part {j} accuracy:', count)

# ======================================================================================================================

# # # # Case 6:
# # # Count frequence of every partition and calculate accuracy in every partition
#
# import pandas as pd
#
# datasetDF = pd.read_csv('./data/Step_1_Dataset.csv', encoding='big5')
# datasetDF = datasetDF[['date', 'close', 'Score']]
# # datasetDF = datasetDF.iloc[-100:,].reset_index(drop=True)
# datasetDF['TP/TN'] = None
# latter = datasetDF['close'].iloc[1:].reset_index(drop=True)
# former = datasetDF['close'].iloc[:-1].reset_index(drop=True)
# closeSpread = latter - former
# closeFirstDay = 183 - 181.5
# closeSpread = pd.concat([pd.Series([closeFirstDay]), closeSpread], axis=0).reset_index(drop=True)
#
#
# # T: Correctly recognize the sample
# # F: Uncorrectly recognize the sample
# # P: the sample belongs to A category (stock price rise)
# # N: the sample belongs to B category (stock price fall)
#
# for q in range(0, 800, 100):
#     print(f'{q}~{q + 100}')
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     for i in range(len(closeSpread)):
#         if q+100 > datasetDF['Score'][i] >= q:
#             # Stock price rise
#             if closeSpread[i] >= 0:
#                 if datasetDF['Score'][i] >= 0:
#                     TP += 1
#                     datasetDF['TP/TN'][i] = datasetDF['Score'][i]
#                     datasetDF['Score'][i] = None
#                 else:
#                     FP += 1
#             # Stock price fall
#             else:
#                 if datasetDF['Score'][i] < 0:
#                     TN += 1
#                     datasetDF['TP/TN'][i] = datasetDF['Score'][i]
#                     datasetDF['Score'][i] = None
#                 else:
#                     FN += 1
#     if (TP+TN+FP+FN) == 0:
#         continue
#     accuracy = (TP+TN) / (TP+TN+FP+FN)
#     precision = TP / (TP + FP)
#     recall = TP / (TP + FN)
#     f1 = 2 * precision * recall / (precision + recall)
#     print(f'Accuracy at {q}~{q+100}:', accuracy)
#     print(f'Count at {q}~{q + 100}:', (TP + TN + FP + FN))
#
#
# for q in range(0, 300, 100):
#     q = -q
#     print(f'{q}~{q + 100}')
#     TP = 0
#     TN = 0
#     FP = 0
#     FN = 0
#     for i in range(len(closeSpread)):
#         if q+100 > datasetDF['Score'][i] >= q:
#             # Stock price rise
#             if closeSpread[i] >= 0:
#                 if datasetDF['Score'][i] >= 0:
#                     TP += 1
#                     datasetDF['TP/TN'][i] = datasetDF['Score'][i]
#                     datasetDF['Score'][i] = None
#                 else:
#                     FP += 1
#             # Stock price fall
#             else:
#                 if datasetDF['Score'][i] < 0:
#                     TN += 1
#                     datasetDF['TP/TN'][i] = datasetDF['Score'][i]
#                     datasetDF['Score'][i] = None
#                 else:
#                     FN += 1
#     print(f'Count:', (TP + TN + FP + FN))
#     if (TP+TN+FP+FN) != 0:
#         accuracy = (TP+TN) / (TP+TN+FP+FN)
#         print(f'Accuracy:', accuracy)
#
#
#     if (TP + FP) != 0:
#         precision = TP / (TP + FP)
#         print(f'precision:', precision)
#
#     if (TP + FN) != 0:
#         recall = TP / (TP + FN)
#         print(f'recall:', recall)
#     if (precision + recall) != 0:
#         f1 = 2 * precision * recall / (precision + recall)
#         print(f'f1:', f1)


