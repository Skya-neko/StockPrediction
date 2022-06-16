import itertools
import numpy as np
Dense1List = np.random.randint(1, 144, size=3).tolist()
Dense2List = np.random.randint(1, 144, size=3).tolist()
learning_rateList = [0.00001]
learning_rateList = [0.00001]


def para(Dense1Units, Dense2Units, learning_rate):
    paramDict = {
        # In tuning, random_seed is not important in statistic result
        'random_seed': 200,
        'Dense1Units': Dense1Units,
        'Dense2Units': Dense2Units,
        'learning_rate': learning_rate,
    }
    print(paramDict)


for i in itertools.product(Dense1List, Dense2List, learning_rateList):
    print(i)
    print(type(i))
    para(*i)


# for Dense1Units in Dense1List:
#     for Dense2Units in Dense2List:
#         for learning_rate in [1]:
#             learning_rate = learning_rate / 100000
#             for decay in [0]:
#                 decay = decay / 100
#                 for momentum in [9]:
#                     momentum = momentum / 10
#                     for epochs in [2000]:
#                         for batch_size in [10]:
#                             paramDict = {
#                                 # In tuning, random_seed is not important in statistic result
#                                 'random_seed': 200,
#                                 'Dense1Units': Dense1Units,
#                                 'Dense2Units': Dense2Units,
#                                 'learning_rate': learning_rate,
#                                 'decay': decay,
#                                 'momentum': momentum,
#                                 'nesterov': True,
#                                 'optimizer': 'sgd',
#                                 'loss': 'mean_squared_error',
#                                 'epochs': epochs,
#                                 'verbose': 0,
#                                 'batch_size': batch_size,
#                             }

