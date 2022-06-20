schtasks /create  /sc minute  /mo 30 /sd 2022/06/17 /st 22:50 /ed 2022/07/10 /tn ANN_Two /tr  D:\StockPrediction\StockPrediction\package\Step_1_ANN_Two_CombineCSV_Run.bat
schtasks | find "ANN_Two"
pause
@REM schtasks /delete /tn ANN_Two ::Delete the job
@REM cmd /k ::If you want cmd.exe not to close to be able to remain typing, use cmd /k command at the end of the file.