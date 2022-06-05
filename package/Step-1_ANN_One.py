import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("TkAgg")
print(matplotlib.get_backend())
import matplotlib.pyplot as plt
import time   # 計算function執行時間
from datetime import datetime
import math

from tensorflow.compat.v1.keras import Sequential
from tensorflow.compat.v1.keras.layers import Dense
from tensorflow.compat.v1.keras.optimizers import SGD

#可以調整Dense權重參數的模組


from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error
import joblib


    
def CombData(pred):
    #在前95%的交易日中，設定預測結果和收盤價一致
    sameDays = len(datasetDf) - len(pred)                 #預測結果和收盤價一致的天數
    datasetDf.loc[:,'predictedValue'] = datasetDf.loc[:,'close']  #預測結果跟收盤價一致，所以複製DataFrame的close欄數值，並貼上到df新宣告的predictedValue欄
    
    
    #在後5%的交易日中，用測試集推算預測股價，用預測的資料蓋掉原後5%的資料
    datasetDf.loc[sameDays:,'predictedValue'] = pred


def PltCombData( ):       

    pltStart = int(len(datasetDf)*7/10)
   
    plt.figure(figsize=(25,10))
    plt.title('Artificial Neural Network',fontsize=25)
    datasetDf['close'][pltStart:].plot(color='blue', label='Real Data')
    datasetDf['predictedValue'][pltStart:].plot(color='red', label='predicted Data')
    plt.legend(loc='best',fontsize=18)
    
    #設定x座標的標籤
    count10 = datasetDf[pltStart:].index%10==0                          #返回True False陣列
    major_index=datasetDf[pltStart:].index[count10]
    major_xtics=datasetDf['date'][pltStart:][major_index]               #這邊的major_index換成count10也可以唷
    plt.xticks(major_index, major_xtics,fontsize=16)                #參數1填入刻度位，參數2填入於該刻度的標籤
    plt.setp(plt.gca().get_xticklabels(),rotation=30)   #旋轉x軸標籤，以免每一個都是橫的顯示會看不清楚
    
    #設定樣式
    plt.grid(linestyle='-.')                            #在圖上顯示網底
    plt.savefig('./data/Step-0_ANNOneResult.png')
    plt.close()   #prevent matplotlib auto plot
    # plt.show()
        


datasetDf = pd.read_csv('./data/Step-1_Dataset.csv',encoding='big5')

#劃分特徵值和目標值(都要變成ndarray才可以輸入train_test_split
feature = datasetDf.iloc[:,~datasetDf.columns.isin(['date','close'])]#.values                        #單獨抓出feature的值，並將其指定給feature。對df使用values函式後，資料型態就會變成ndarray
target = np.array(datasetDf['close'])                    #將df中的'close'欄位，存成numpy的array



#劃分訓練集，測試集
# if preprocessing:
#     feature = scale(feature)
feature_train, feature_test,target_train, target_test = train_test_split(feature, target, test_size = 0.25,shuffle = False)  #因為shuffle = False所以不用random_state=10,
predictedDays = int(math.ceil(0.25*len(target) )) #int(math.ceil(testSize*( len(data) - nDay )))               #pridectedDays用模型預測出的數據天數 - (nPeriod-1) 

scaler = joblib.load(r'.\data\Step-1_Scaler.gz')
feature_train_scaled = scaler.fit_transform(feature_train)


def iterate(func):
    # optimizerList = ['sgd']
    # lossList = ['mean_squared_error']
    # for optimizer in optimizerList:
    #     for loss in lossList:
    # for random_seed in [0,100,200]:
    for i_execute in range(0,20): 
        for Dense1Units in [128,256]:
            for Dense2Units in [32,38,46]:
            #     for Dense3Units in [64]:
                # for Dense4Units in [32]:
                    for learning_rate in [1]:
                        learning_rate = learning_rate/100000
                        for decay in [0]:
                            decay = decay/100
                            for momentum in [9]:
                                momentum = momentum /10
                                for epochs in [2000, 3000]:
                                    for batch_size in [0, 10]:                                            
                                        paramDict = {
                                            # 'random_seed': random_seed,
                                            'Dense1Units': Dense1Units,
                                            'Dense2Units': Dense2Units,
                                            # 'Dense3Units': Dense3Units,
                                            # 'Dense4Units': Dense4Units,
                                            'learning_rate': learning_rate,
                                            'decay': decay,
                                            'momentum': momentum,
                                            'nesterov' : True,
                                            'optimizer' : 'sgd',
                                            'loss': 'mean_squared_error',
                                            'epochs': epochs,
                                            'verbose': 0,
                                            'batch_size': batch_size,
                                            }
                                        print('Input')
                                        print(str(paramDict).replace(', ',',\n').replace("{'","{\n'").replace("}","\n}"))
                                        func(paramDict)

    
# paramDict = {
#     'random_seed': 3,
#     'Dense1Units': 256,
#     'Dense2Units': 256,
#     'Dense3Units': 256,
#     'Dense4Units': 256,#256
#     'learning_rate': 0.00001,
#     'decay': 0,
#     'momentum': 0.9,
#     'nesterov' : True,
#     'optimizer' : 'sgd',
#     'loss': 'mean_squared_error',
#     'epochs': 2000,
#     'verbose': 0,
#     'batch_size': 20,
#     }
    
def main(paramDict):

    
    
    print('Execute')
    t0 = time.time()
    # set_random_seed(paramDict['random_seed'])
    
    # init_constant = initializers.Constant(value=0.1)
    # init_random = initializers.RandomNormal(seed=1)
    
    model = Sequential()
    model.add(Dense(units = paramDict['Dense1Units'], activation = 'relu', input_dim=feature_train_scaled.shape[1], ))
    model.add(Dense(units = paramDict['Dense2Units'], activation = 'relu', ))
    # model.add(Dense(units = paramDict['Dense3Units'], activation = 'relu', ))
    # model.add(Dense(units = paramDict['Dense4Units'], activation = 'relu', ))
    model.add(Dense(units = 1, ))
    
    sgd = SGD(learning_rate=paramDict['learning_rate'], decay=paramDict['decay'], momentum=paramDict['momentum'], nesterov=paramDict['nesterov'])
    model.compile(optimizer = sgd,loss = paramDict['loss'])
    model.fit(feature_train_scaled, target_train, epochs = paramDict['epochs'], verbose=paramDict['verbose'], batch_size = paramDict['batch_size'],shuffle=False)   
    
    
    
    
    
    feature_test_scaled = scaler.transform(feature_test)
    pred =  model.predict(feature_test_scaled)
    
    score = model.evaluate(feature_test_scaled, target_test,verbose=1)
    # print(score)
    model.summary()
    
    CombData(pred)
    
    
    
    PltCombData()
    try:
        rmse = mean_squared_error(target_test, pred, squared=False)
        # print(rmse)
        rmseStr = str(rmse)[:7].replace('.','_')
        
        t1 = time.time()
        
        
        outputFilePath = './data/'
        outputFileName = 'rmseBeyond5'
        
        if rmse < 10:
            # if not  os.path.exists(outputFilePath):
            #     os.mkdir(outputFilePath)
            outputFileName =  'keras_'+rmseStr+'.h5'
            model.save(outputFilePath + outputFileName)
            
        recordDict = {
            'modelName': outputFileName,
            'score': score,
            'rmse': rmse,
            'spendTime': t1-t0,
            'executionTime(s)': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            }
        print('Output')
        print(str(recordDict).replace(', ',',\n').replace("{'","{\n'").replace("}","\n}"))
        recordDict.update(paramDict)
        rowDf  = pd.DataFrame([recordDict], columns=recordDict.keys())
        
        # init record file
        # rowDf.to_csv(outputFilePath+'Step-0_ANNOneResult.csv', encoding='big5', index=False)#init record file
        # recordDf = pd.read_csv(outputFilePath+'Step-0_ANNOneResult.csv', index_col=False).head(0)  #init record file
        
        recordDf = pd.read_csv(outputFilePath+'Step-0_ANNOneResult.csv', index_col=False)
        recordDf = pd.concat([recordDf, rowDf], axis = 0).reset_index()
        try:
            recordDf = recordDf.drop(['index'], axis = 1)
            recordDf = recordDf.drop(['level_0'], axis = 1)
        except KeyError:
            print('no level_0 or index column')
        # recordDf = recordDf.drop([0,1,2,3])
        finally:
            recordDf.to_csv(outputFilePath+'Step-0_ANNOneResult.csv', encoding='big5', index=False)
    except ValueError:
        print("module can't converge")
        
    del model
    del recordDf
        

# main()

iterate(main)


