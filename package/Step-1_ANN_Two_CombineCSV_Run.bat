set  project_root=D:\StockPrediction\StockPrediction\
cd /d %project_root%
echo Project root: %project_root%
SET "today=%date:~0,10%"
python   %project_root%\package\Step-1_CombineCSV.py  Step-0_ANN_Two_Result_ProcessA.csv  Step-0_ANN_Two_Result_ProcessB.csv  Step-0_ANN_Two_Result.csv  >>  %project_root%\log\Step-1_ANN_Two_CombineCSV_%today:/=-%.txt  2>&1
@REM pause :: schtask will make job run in backgroun, so don't pause because the window keep show up is annoying.
@REM %today:/=-% Means replace "/" with "-"