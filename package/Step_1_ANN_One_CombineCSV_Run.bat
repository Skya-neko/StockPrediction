set  project_root=D:\StockPrediction\StockPrediction\
cd /d %project_root%
echo Project root: %project_root%
SET "today=%date:~0,10%"
python   %project_root%\package\Step_1_CombineCSV.py  Step_0_ANN_One_Result_ProcessA.csv  Step_0_ANN_One_Result_ProcessB.csv  Step_0_ANN_One_Result.csv  >>  %project_root%\log\Log-ANN_One_CombineCSV_%today:/=-%.txt  2>&1
@REM pause :: schtask will make job run in backgroun, so don't pause because the window keep show up is annoying.
@REM %today:/=-% Means replace "/" with "-"