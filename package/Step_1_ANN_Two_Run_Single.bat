cd ../
set  project_root=%cd%
echo Project root: %project_root%
SET "today=%date:~0,10%"
python   %project_root%\package\Step_1_ANN_Two.py Step_0_ANN_Two_Result.csv Single >>   %project_root%\log\Log-ANN_Two_Result_Single_%today:/=-%.txt  2>&1
pause :: Keep the window open
@REM %today:/=-% Means replace "/" with "-"