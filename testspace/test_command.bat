cd ../
set  project_root=%cd%
echo Project root: %project_root%
SET "today=%date:~0,10%"
python   %project_root%\package\Step_1_ANN_Two.py Step_0_ANN_Two_Result_ProcessA.csv >>   %project_root%\log\Step_0_Log_ProcessA_%today:/=-%.txt  2>&1

@REM %today:/=-% Means replace "/" with "-"