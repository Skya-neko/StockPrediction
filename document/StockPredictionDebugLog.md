# StockPredictionDebugLog

## Data

就算我用del model也解決不了data leak的狀況，
![memory leak](https://i.imgur.com/t8OvnYc.png)

使用memory_profiler plot觀察到會有data leak的情況，
並從每執行一行程式所增加的記憶體來查看，
會發現每一次的記憶體增長都發生在model.fit的時候：
![increate at line "model.fit"](https://i.imgur.com/h8xE4TO.png)
查找網路上釋放model.fit記憶體的解法，有人說使用multiproces解決

[keras-release-memory-after-finish-training-process](https://stackoverflow.com/questions/51005147/keras-release-memory-after-finish-training-process)
