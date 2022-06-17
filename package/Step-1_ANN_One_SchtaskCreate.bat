schtasks /create  /sc minute  /mo 5 /sd 2022/06/17 /st 22:50 /ed 2022/07/10 /tn ANN_One /tr  D:\StockPrediction\StockPrediction\package\Step-1_ANN_One_CombineCSV_Run.bat
schtasks | find "ANN_One"
pause
@REM schtasks /delete /tn ANN_One ::Delete the job
@REM cmd /k ::If you want cmd.exe not to close to be able to remain typing, use cmd /k command at the end of the file.