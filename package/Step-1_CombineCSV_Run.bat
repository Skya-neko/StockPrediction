set  project_root=D:\StockPrediction\StockPrediction\
cd /d %project_root%
echo Project root: %project_root%
SET "today=%date:~0,10%"
python   %project_root%\package\Step-1_CombineCSV.py  Step-0_ANNTwoResult_ProcessA.csv  Step-0_ANNTwoResult_ProcessB.csv  Step-0_ANNTwoResult.csv  >>  %project_root%\log\Step-1_CombineCSV_%today:/=-%.txt  2>&1
pause :: Keep the window open
@REM %today:/=-% Means replace "/" with "-"