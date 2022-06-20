# Stock-Prediction-Debug-Log

## Data Leak

就算我用del model也解決不了data leak的狀況，

![memory leak](https://i.imgur.com/t8OvnYc.png)

使用memory_profiler plot觀察到會有data leak的情況，
並從每執行一行程式所增加的記憶體來查看，
會發現每一次的記憶體增長都發生在model.fit的時候：

![increate at line "model.fit"](https://i.imgur.com/h8xE4TO.png)

查找網路上釋放model.fit記憶體的解法，有人說使用multiproces解決：
![sucess release](https://i.imgur.com/AHvEqqI.png)
[keras-release-memory-after-finish-training-process](https://stackoverflow.com/questions/51005147/keras-release-memory-after-finish-training-process)

原因是因為在主進程import keras就會生成一個新的進程就會導致這種狀況，因此得在子進程import keras，將model輸出後的結果使用multiprocess.Queue傳遞到主進程。
[keras generate new process](https://stackoverflow.com/questions/42504669/keras-tensorflow-and-multiprocessing-in-python)


### Solution: Multiprocess


#### Interprocesses communication code
```python=
from multiprocessing import Process, Queue

def square(numbers, queue):
    for i in numbers:
        queue.put(i*i)  # First in First out
        
def main():
    numbers = range(5)
    queue = Queue()
    square_process = Process(target=square, args=(numbers, queue))
    square_process.start()  
    square_process.join()  # Continue the main process after execution of child process
    print('end of child process')
    while not queue.empty():
        print(queue.get())   # First in First out

if __name__ == '__main__':
    main()
```

#### Pycharm can't execute multiprocess
而在使用pycharm執行Multiprocess腳本時，`square_process.start()`發生錯誤
```bash=
Traceback (most recent call last):
  File "C:\Users\Vivian\anaconda3\lib\site-packages\IPython\core\interactiveshell.py", line 3343, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-2-2adf49e4d7c5>", line 1, in <module>
    runfile('D:/StockPrediction/StockPrediction/testspace/MultiprocessComunicationGuide.py', wdir='D:/StockPrediction/StockPrediction')
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2021.3.1\plugins\python-ce\helpers\pydev\_pydev_bundle\pydev_umd.py", line 198, in runfile
    pydev_imports.execfile(filename, global_vars, local_vars)  # execute the script
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2021.3.1\plugins\python-ce\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "D:/StockPrediction/StockPrediction/testspace/MultiprocessComunicationGuide.py", line 21, in <module>
    main()
  File "D:/StockPrediction/StockPrediction/testspace/MultiprocessComunicationGuide.py", line 11, in main
    square_process.start()
  File "C:\Users\Vivian\anaconda3\lib\multiprocessing\process.py", line 121, in start
    self._popen = self._Popen(self)
  File "C:\Users\Vivian\anaconda3\lib\multiprocessing\context.py", line 224, in _Popen
    return _default_context.get_context().Process._Popen(process_obj)
  File "C:\Users\Vivian\anaconda3\lib\multiprocessing\context.py", line 326, in _Popen
    return Popen(process_obj)
  File "C:\Users\Vivian\anaconda3\lib\multiprocessing\popen_spawn_win32.py", line 93, in __init__
    reduction.dump(process_obj, to_child)
  File "C:\Users\Vivian\anaconda3\lib\multiprocessing\reduction.py", line 60, in dump
    ForkingPickler(file, protocol).dump(obj)
_pickle.PicklingError: Can't pickle <function square at 0x0000012219CC4040>: attribute lookup square on __main__ failed
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\Vivian\anaconda3\lib\multiprocessing\spawn.py", line 116, in spawn_main
    exitcode = _main(fd, parent_sentinel)
  File "C:\Users\Vivian\anaconda3\lib\multiprocessing\spawn.py", line 126, in _main
    self = reduction.pickle.load(from_parent)
EOFError: Ran out of input
```

原因在[multiprocessing in PyCharm results in _pickle.PicklingError](https://stackoverflow.com/questions/70947312/multiprocessing-in-pycharm-results-in-pickle-picklingerror)中有解釋
> It's not possible in Windows. You are trying to run code that doesn't work in interactive mode. But turns out PyCharm runs the code as a script and it is a bug.

#### CMD can execute multiprocess
因此單純的使用CMD執行就會成功
![CMD run multiprocess](https://i.imgur.com/FD1CcIC.png)


我需要宣告一個train model的function，
並使用Queue從child process中蒐集模型的訓練成果到main process：
| variable            | data type | description               |
|:------------------- | --------- |:------------------------- |
| pred                | ndarray   | predict result            |
| score               | float     | model train score         |
| short_model_summary | string    | print model.summary()     |
| t0                  | float     | start model training time |

#### Observe memory usage with memory_profiler
[How to profile multiple subprocesses using Python multiprocessing and memory_profiler?](https://stackoverflow.com/questions/38358881/how-to-profile-multiple-subprocesses-using-python-multiprocessing-and-memory-pro)
```bash=
$ mprof run -M python myscript.py
$ mprof plot
```
可以看到將train model的部分使用child process執行程式後，
就不會再有memory leak的狀況了！
![](https://i.imgur.com/ppNtgUj.png)
![](https://i.imgur.com/K2keqH2.png)


### Discussion: maybe the data leak problem is caused by I use v1 tensorflow to train model
因為別人沒有遇到這種情況...
所以使用最新版的tensorflow看看(目前最新版是2.9.1)

[Memory leak in model.fit](https://github.com/tensorflow/tensorflow/issues/37505)
這個討論最後指出在tensorflow 2.3->2.4有解決這個問題，

而我原本使用的是2.8.0版本，問題應該要已經被解決了才是?
細究我使用的module
```python=
from tensorflow.compat.v1.keras import Sequential
from tensorflow.compat.v1.keras.layers import Dense
from tensorflow.compat.v1.keras.optimizers import SGD
from tensorflow.compat.v1 import set_random_seed
```
[Tensorflow Core v 2.8.0 tensorflow.compat.v1.keras 官方文檔](https://www.tensorflow.org/versions/r2.8/api_docs/python/tf/compat/v1/keras)
> Public API for tf.keras namespace.

[Tensorflow Core v 2.9.1 tensorflow.compat.v1.keras 官方文檔](https://www.tensorflow.org/api_docs/python/tf/compat/v1/keras)
> Implementation of the Keras API, the high-level API of TensorFlow.
Detailed documentation and user guides are available at keras.io.

看2.9.1的敘述才比較了解，原來使用這種引進的模組，只是使用比較 high-level的API而已

會不會是使用了這個high-level API才導致model.fit有memory leak的問題呢?
於是將code改成：
```python=
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import set_random_seed
```
執行看看，才發現還是有memory leak的問題：
![](https://i.imgur.com/ZwVheuA.png)

最終的結論是，到tensorflow 2.8.0 memory leak的問題都沒有解決，
但因為我的環境不允許我裝2.9.1，覺得也不用大費周章測試2.9.1有沒有解決了，
只要使用multiprocess的解決方案就好！


## Train model with GPU

### Prepare conda venv
[Train model with GPU - Tensorflow official guide](https://www.tensorflow.org/install/pip#windows_1)
點選上面的網站，如果顯示其他國語言則只要在右上角切換語言就好
下拉到Step-by-step教學
1. Install Microsoft Visual C++ Redistributable
> The Visual C++ Redistributable installs Microsoft C and C++ (MSVC) runtime libraries.
> The redistributable comes with Visual Studio 2019 but can be installed separately

下載後重啟後，Make sure long paths are enabled on Windows.
![](https://i.imgur.com/NxyV34W.png)

2. 已經安裝完整的Anaconda了，不用安裝miniconda，因此直接在cmd上建置conda環境，(像是建立pycharm的虛擬環境，套件包各自獨立)
```bash=
conda create --name tf python=3.9
```
3. 到虛擬環境下完成剩下的安裝步驟
```bash=
conda activate tf
```
![](https://i.imgur.com/kqwTANC.png)

4. 在這一步開始了解為甚麼要用conda建置虛擬環境了！
```bash=
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
```
[only can use conda install cudatoolkit](https://stackoverflow.com/questions/67912832/why-cant-i-install-cudatookkit-10-1-using-pip-but-can-using-conda)
> The reason why cudatoolkit is not available in pypi is because it's not a python packge. It is a toolkit from nvidia that needs a C compiler to exist in your system. Pip was never intended to handle such cases, whereas Anaconda is.

直至此步驟所安裝的package有：
![](https://i.imgur.com/AFy5E1l.png)


5. 在conda虛擬環境中使用pip下載pypi中的tensorflow
```bash=
pip install tensorflow
```
6. 在conda虛擬環境中執行python測試使否可正常使用tensorflow
```bash=
python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```


### Execute script on conda venv
如果要執行自己的腳本，也是在這個環境中直接用python執行就好囉！
首先cd 到D槽，使用`cd D:\foldername`無法切換成功，因為：
> cd D:\foldername changes D:'s current directory to the foldername specified, but does not change the fact that you're still working on the C: drive.

所以要加一個 `/d`
```bash=
cd /d D:\ANN_Execution_Init\
```
> The /d switch will change the current directory of the specified drive AND change to that directory. The /d switch must be specified before the path.



### Run with GPU even slower than with CPU...
GPU跑一次500秒，CPU跑一次90秒...
[Training a simple model in Tensorflow GPU slower than CPU](https://stackoverflow.com/questions/55749899/training-a-simple-model-in-tensorflow-gpu-slower-than-cpu)
>　the overhead of invoking GPU kernels, and copying data to and from GPU, the cost is very high.

### What if run two bat file in parallel?
測試的結果，就是可以清楚地從工作管理員看到，兩個process競爭GPU資源的狀況...
只會變得很慢很慢

### Distributed train model
結果有其他可以分散式訓練模型的方法嗎？
遺憾的是，沒有找到...

### Summary
繼續使用CPU訓練還比較快~~  認命吧QQ


## Observation of Execution on Computers

### My laptop
#### ANN_Two execute with single process 
擷取44筆資料算平均，去掉離群值，平均在180秒(3分鐘)內會跑完一個模型)
![](https://i.imgur.com/FSHpEk7.png)
那個離群值是我沒有使用電腦的時段造成的，
所以先把睡眠調成永不看看！

#### ANN_Two execute with double process
暫時只看3筆，差不多落在185左右

### zzser
#### ANN_Two execute with triple process 
同時執行(一個ANN_Two在D槽一個在桌面)processA,B和Single，
每一個模型大約跑150秒。
![](https://i.imgur.com/5P4ba0P.png)
確實辦到算力平行。

但後來發現，

## Connect to SQL Server
想要使用pandas x sqlalchemy的組合，
就必須先裝好pymssql or pyodbc，
他們是python的SQL驅動程式。


### pymssql connection
[open up TCP/IP access for my local SQL server.](https://stackoverflow.com/questions/19348255/pymssql-operationalerror-db-lib-error-message-20009-severity-9)
```python=
from pymssql import connect
server = 'localhost'  # DESKTOP-2LNIJAK\SQLEXPRESS'
username = 'Vivian'
password = ''
master_database_name = 'traing_result'
port = 1433
server_args = {'server': server, 'user': username, 'password': password,
               'database': master_database_name, 'port': port}
master_database = connect(**server_args)
```
連線到SQL解決！


但
```bash=
Traceback (most recent call last):
  File "src\pymssql\_pymssql.pyx", line 646, in pymssql._pymssql.connect
  File "src\pymssql\_mssql.pyx", line 2108, in pymssql._mssql.connect
  File "src\pymssql\_mssql.pyx", line 700, in pymssql._mssql.MSSQLConnection.__init__
  File "src\pymssql\_mssql.pyx", line 1817, in pymssql._mssql.maybe_raise_MSSQLDatabaseException
  File "src\pymssql\_mssql.pyx", line 1834, in pymssql._mssql.raise_MSSQLDatabaseException
pymssql._mssql.MSSQLDatabaseException: (18456, b"\xe4\xbd\xbf\xe7\x94\xa8\xe8\x80\x85 'Vivian' \xe7\x9a\x84\xe7\x99\xbb\xe5\x85\xa5\xe5\xa4\xb1\xe6\x95\x97\xe3\x80\x82DB-Lib error message 20018, severity 14:\nGeneral SQL Server error: Check messages from the SQL Server\nDB-Lib error message 20002, severity 9:\nAdaptive Server connection failed (localhost)\nDB-Lib error message 20002, severity 9:\nAdaptive Server connection failed (localhost)\n")
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "C:\Users\Vivian\anaconda3\lib\site-packages\IPython\core\interactiveshell.py", line 3343, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-2-3bc8450fd07d>", line 1, in <module>
    runfile('D:/StockPrediction/StockPrediction/testspace/test_sqlserverConn.py', wdir='D:/StockPrediction/StockPrediction')
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2021.3.1\plugins\python-ce\helpers\pydev\_pydev_bundle\pydev_umd.py", line 198, in runfile
    pydev_imports.execfile(filename, global_vars, local_vars)  # execute the script
  File "C:\Program Files\JetBrains\PyCharm Community Edition 2021.3.1\plugins\python-ce\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "D:/StockPrediction/StockPrediction/testspace/test_sqlserverConn.py", line 9, in <module>
    master_database = connect(**server_args)
  File "src\pymssql\_pymssql.pyx", line 652, in pymssql._pymssql.connect
pymssql._pymssql.OperationalError: (18456, b"\xe4\xbd\xbf\xe7\x94\xa8\xe8\x80\x85 'Vivian' \xe7\x9a\x84\xe7\x99\xbb\xe5\x85\xa5\xe5\xa4\xb1\xe6\x95\x97\xe3\x80\x82DB-Lib error message 20018, severity 14:\nGeneral SQL Server error: Check messages from the SQL Server\nDB-Lib error message 20002, severity 9:\nAdaptive Server connection failed (localhost)\nDB-Lib error message 20002, severity 9:\nAdaptive Server connection failed (localhost)\n")
```
這是什麼????QQ

查了錯誤18456，原來是userName輸入錯了
```python=
from pymssql import connect
server = 'localhost:57226'  # DESKTOP-2LNIJAK\SQLEXPRESS'
username = r'DESKTOP-2LNIJAK\Vivian'
password = ''
master_database_name = 'traing_result'
port = 1433
server_args = {'server': server, 'user': username, 'password': password,
               'database': master_database_name, 'port': port, 'charset': 'UTF-8'}
conn = connect(**server_args)
if conn:
    print('Connect!')

```
這樣的程式碼才對！
1. 開啟TCP動態端口，並實現到程式碼上
2. 可以從Server中的Securities看到，現在有哪些可以進Server的使用者!
![](https://i.imgur.com/DBd9FHF.png)

[18456教學1](https://blog.csdn.net/weixin_42198265/article/details/124840388)
[18456教學2](https://www.liquidweb.com/kb/troubleshooting-microsoft-sql-server-error-18456-login-failed-user/)

### sqlalchemy connection
```python=
from sqlalchemy import create_engine
conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}/?charset=utf8'
engine = create_engine(conn_str)
```
發生了錯誤`ValueError: invalid literal for int() with base 10: '57226:1433'`
於是直接把57226改掉看看，就可以正常運行了(可見在設定pymssql連線的時候，不需要輸入動態端口)
```python=
from pymssql import connect
server = 'localhost'  # DESKTOP-2LNIJAK\SQLEXPRESS'  :57226
username = r'DESKTOP-2LNIJAK\Vivian'
password = ''
database_name = 'traing_result'
port = 1433
server_args = {'server': server, 'user': username, 'password': password,
               'database': database_name, 'port': port, 'charset': 'UTF-8'}
conn = connect(**server_args)
if conn:
    print('Connect!')
conn.close()

from sqlalchemy import create_engine
conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}/?charset=utf8'
engine = create_engine(conn_str)
```
一切可以正常運作了！


### Use sqlalchemy and pandas communicate with SQL Server
```python=
# pandas & sqlalchemy application
recordDF = pd.read_csv('./data/Step-0_ANN_Two_Result.csv',index_col=False)
recordDF.to_sql('Step-0_ANN_Two_Result_20220620', con=engine)
```
使用上面的程式還沒問題，結果到了to_sql又出現了18456的錯誤了QQ
![](https://i.imgur.com/0146kw0.png)

於是先嘗試用pymssql拿到sql table的資料(Success)，
再嘗試用sqlalchemy拿資料(fail)，使用sqlalchemy拿資料的時候卻發生了18456錯誤，
但是把connectionString裡的charset移除，就運作正常了。
[removed the charset option](https://stackoverflow.com/questions/66434480/python-pymssql-error-18456-bdb-lib-error-message-20010-severity-8-nunable-t)

接下來繼續嘗試使用pandas的read_sql()和to_sql()，
怪了pymssql和sqlalchemy都可以正常運行了但pandas.read_sql()還是不行，
發生錯誤2809 `sqlalchemy.exc.OperationalError: (pymssql._pymssql.OperationalError) (2809, `
據[sqlalchemy官方](https://docs.sqlalchemy.org/en/13/errors.html#error-e3q8)的說法
operation error是連接到DB上的錯誤，並且是根源於pymssql的錯誤，
跟sqlalchemy沒關係

原本的程式碼是這樣：
```python=
table = pd.read_sql('dbo.[Step-0_ANN_Two_Result_20220619]', con=engine)
```
後來查到[調用獲取表值參數的存儲過程時出現錯誤 2809](https://support.microsoft.com/en-us/topic/kb3205935-fix-error-2809-when-you-execute-a-stored-procedure-that-takes-a-table-valued-parameter-from-rpc-calls-in-sql-server-2014-or-2016-adfa8855-d272-ce13-a754-2eafe0106652)

發現表明再python腳本應該寫成：
```python=
table = pd.read_sql('Step-0_ANN_Two_Result_20220619', con=engine)
```
就可以正常運行了！





## Train redundant model
### ProcessA, Process B flaws
![](https://i.imgur.com/9PNe0Di.png)
可以從上圖看到，假設綠色的結果是由ProcessA產生，
因為程式只有check Resault.csv，並沒有check Resault_ProcessA.csv，
造成五分鐘內會跑同一組參數的模型，五分鐘內可以跑四支模型，
但卻因為只有check Result.csv，變成五分鐘內只跑一個我不要的模型...
Debug!
程式中加入check Resault_ProcessA.csv


## Contents on paper
硬體環境、每個硬體環境配上process的運行時間。


把為甚麼選台積電三星英特爾三家的原因寫進去