# Stock Trend Prediction with ANN 
基於財經字典與分析指標的神經網路預測股價趨勢

Predicting stock price trend using neural network based on financial lexicon and technical indicator

## 主要目的
本研究旨在使用多元線性迴歸模型 (multiple linear regression) 和人工神經網
路模型 (Artificial neural network) 預測股價，以有大量新聞的公司台積電作為研
究對象，擷取其在新聞、分析指標、歷史股價上的多方資訊。本文蒐集來自富
果網站上的財金新聞，並將財金新聞做「台積電」、「大盤相關新聞」兩大分
類，使用自製情感字典計算出兩大分類的新聞情緒分數，自製爬蟲程式蒐集台
積電的分析指標與歷史股價，最後將兩大新聞情緒分數、分析指標、歷史股價
作為預測股價的特徵。



## 主要功能
+ 抓取近5年新聞資料
+ 抓取16個分析指標
+ 抓取歷史股價
+ 運算情感分數
+ 訓練模型
+ 預測明日股價
+ 模擬投資


## 模型成效



