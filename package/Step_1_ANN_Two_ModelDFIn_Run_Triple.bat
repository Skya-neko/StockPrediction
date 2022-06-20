cd ../
set  project_root=%cd%
echo Project root: %project_root%
SET "today=%date:~0,10%"
start    python   .\package\Step_1_ANN_Two.py Step_0_ANN_Two_Result_ProcessC.csv Triple >>   .\log\Log-ANN_Two_Result_ProcessC_%today:/=-%.txt  2>&1
rem // Allow a key-press to abort the wait; `/T` can be omitted:
timeout /T 5
timeout 5
@REM  Sleep for 5 seconds avoid process execute tensorflow simultaneously
start    python   .\package\Step_1_ANN_Two.py Step_0_ANN_Two_Result_ProcessD.csv Triple >>   .\log\Log-ANN_Two_Result_ProcessD_%today:/=-%.txt  2>&1
rem // Allow a key-press to abort the wait; `/T` can be omitted:
timeout /T 5
timeout 5
start    python   .\package\Step_1_ANN_Two.py Step_0_ANN_Two_Result_ProcessE.csv Triple >>   .\log\Log-ANN_Two_Result_ProcessE_%today:/=-%.txt  2>&1
pause :: Keep the window open
@REM %today:/=-% Means replace "/" with "-"