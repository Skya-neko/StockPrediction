# =============================================================================
# import module
# =============================================================================
#資料分析套件
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#sklearn 線性迴歸
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import  PolynomialFeatures

#keras LSTM
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

#sklearn MLP
from sklearn.metrics import mean_squared_error



#keras MLP
tf.compat.v1.disable_eager_execution()


    
def CombData(pred):
    #在前95%的交易日中，設定預測結果和收盤價一致
    sameDays = len(datasetDf) - len(pred)                 #預測結果和收盤價一致的天數
    datasetDf.loc[:,'predictedValue'] = datasetDf.loc[:,'close']  #預測結果跟收盤價一致，所以複製DataFrame的close欄數值，並貼上到df新宣告的predictedValue欄
    
    
    #在後5%的交易日中，用測試集推算預測股價，用預測的資料蓋掉原後5%的資料
    datasetDf.loc[sameDays:,'predictedValue'] = pred
        


def PltCombData( ):       
    pltStart = int(len(datasetDf)*7/10)

    plt.figure(figsize=(25,10))
    plt.title('Multiple Linear Regression',fontsize=25)
    datasetDf['close'][pltStart:].plot(color='blue', label='Real Data')
    datasetDf['predictedValue'][pltStart:].plot(color='red', label='predicted Data')
    plt.legend(loc='best',fontsize=18)
    
    #設定x座標的標籤
    count10 = datasetDf[pltStart:].index%10==0                          #返回True False陣列
    major_index=datasetDf[pltStart:].index[count10]
    major_xtics=datasetDf['date'][pltStart:][major_index]               #這邊的major_index換成count10也可以唷
    plt.xticks(major_index, major_xtics,fontsize=16)                    #參數1填入刻度位，參數2填入於該刻度的標籤
    plt.setp(plt.gca().get_xticklabels(),rotation=30)                   #旋轉x軸標籤，以免每一個都是橫的顯示會看不清楚
    
    #設定樣式
    plt.grid(linestyle='-.')                                            #在圖上顯示網底
    plt.savefig('./data/Step-0_MLROneResult.png')
    plt.close()  # prevent matplotlib auto plot
    # plt.show()
        

     

print('執行case: ')
datasetDf = pd.read_csv('./data/Step-1_Dataset.csv',encoding='big5')

#劃分特徵值和目標值(都要變成ndarray才可以輸入train_test_split
feature = datasetDf.iloc[:,~datasetDf.columns.isin(['date','close'])] #單獨抓出feature的值，並將其指定給feature。對df使用values函式後，資料型態就會變成ndarray
target = np.array(datasetDf['close'])                                 #將df中的'close'欄位，存成numpy的array




#劃分訓練集，測試集
feature_train, feature_test,target_train, target_test = train_test_split(feature, target, test_size = 0.25,random_state= 0,shuffle = False)

scaler = MinMaxScaler()
feature_train_scaled = scaler.fit_transform(feature_train)
# if  degree:
#     poly_reg =PolynomialFeatures(degree=degree)              #degree設定幾次多項式
#     feature_train = poly_reg.fit_transform(feature_train)
#     feature_test = poly_reg.fit_transform(feature_test)

#訓練線性迴歸模型
model = LinearRegression()                                  #使用線性模型裡面的線性回歸
model.fit(feature_train_scaled, target_train)               #將特徵值和目標值(多個自變數和一個依變數)餵給模型，並開始做模型擬合
                                                            #fit後，model這個物件就已經被訓練完成，成為我們要拿來預測資料的模型


#用測試集預測結果
feature_test_scaled = scaler.transform(feature_test)
pred = model.predict(feature_test_scaled)                   #predictByTest是預測後得出的收盤價，而他的長度就是pridectedDays
score = round( model.score(feature_test, target_test) , 3 )
      
CombData(pred)
PltCombData()

rmse = mean_squared_error(target_test, pred, squared=False)