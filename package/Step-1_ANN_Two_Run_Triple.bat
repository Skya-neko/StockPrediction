cd ../
set  project_root=%cd%
echo Project root: %project_root%
SET "today=%date:~0,10%"
start %project_root%\package\Step-1_ANN_Two_Run_ProcessC.bat   :: start will create new process for this bat
rem // Allow a key-press to abort the wait; `/T` can be omitted:
timeout /T 5
timeout 5
@REM  Sleep for 5 seconds avoid process execute tensorflow simultaneously
start %project_root%\package\Step-1_ANN_Two_Run_ProcessD.bat
rem // Allow a key-press to abort the wait; `/T` can be omitted:
timeout /T 5
timeout 5
start %project_root%\package\Step-1_ANN_Two_Run_ProcessE.bat
pause :: Keep the window open
@REM %today:/=-% Means replace "/" with "-"