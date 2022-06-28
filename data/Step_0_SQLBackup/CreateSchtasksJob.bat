schtasks /create /sc minute /mo 30 /sd 2022/06/23 /st 12:10 /ed 2022/08/10 /tn ANN_Two_Backup_to_github /tr D:\StockPrediction\StockPrediction\data\Step_0_SQLBackup\Backup_Run.bat
schtasks | find "ANN_Two_Backup_to_github"
pause