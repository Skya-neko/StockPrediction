schtasks /create  /sc minute  /mo 5 /sd 2022/06/17 /st 22:50 /ed 2022/07/10 /tn run_ml /tr  D:\StockPrediction\StockPrediction\package\Step-1_CombineCSV_Run.bat
schtasks | find "run_ml"
pause
@REM schtasks /delete /tn run_ml ::Delete the job
@REM cmd /k ::If you want cmd.exe not to close to be able to remain typing, use cmd /k command at the end of the file.