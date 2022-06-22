cd ../
set  project_root=%cd%
echo Project root: %project_root%
SET "today=%date:~0,10%"
start    python   .\package\Step_1_ANN_Two_ModelDFIn.py Step_0_ANN_Two_Result_ProcessC.csv Triple
rem // Allow a key-press to abort the wait; `/T` can be omitted:
timeout 5
@REM  Sleep for 5 seconds avoid process execute tensorflow simultaneously
start    python   .\package\Step_1_ANN_Two_ModelDFIn.py Step_0_ANN_Two_Result_ProcessD.csv Triple
rem // Allow a key-press to abort the wait; `/T` can be omitted:
timeout 5
start    python   .\package\Step_1_ANN_Two_ModelDFIn.py Step_0_ANN_Two_Result_ProcessE.csv Triple
pause :: Keep the window open
@REM %today:/=-% Means replace "/" with "-"