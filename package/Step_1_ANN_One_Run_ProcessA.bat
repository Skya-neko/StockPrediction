cd ../
set  project_root=%cd%
echo Project root: %project_root%
SET "today=%date:~0,10%"
python   %project_root%\package\Step_1_ANN_One.py Step_0_ANN_One_Result_ProcessA.csv >>   %project_root%\log\Log-ANN_One_Result_ProcessA_%today:/=-%.txt  2>&1
pause :: Keep the window open
@REM %today:/=-% Means replace "/" with "-"