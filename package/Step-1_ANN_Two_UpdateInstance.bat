cd ..\
set  project_root=%cd%
set  instance_root=D:\ANNTwo_CPU
echo Project root: %project_root%
echo instance_root root: %instance_root%
@REM data
xcopy  %project_root%\data\Step-0_ANN_Two_Result.csv  %instance_root%\data\Step-0_ANN_Two_Result.csv  /Y
xcopy  %project_root%\data\Step-0_ANN_Two_Result_ProcessA.csv  %instance_root%\data\Step-0_ANN_Two_Result_ProcessA.csv  /Y
xcopy  %project_root%\data\Step-0_ANN_Two_Result_ProcessB.csv  %instance_root%\data\Step-0_ANN_Two_Result_ProcessB.csv  /Y
xcopy  %project_root%\data\Step-1_Dataset.csv  %instance_root%\data\Step-1_Dataset.csv  /Y
@REM package
xcopy  %project_root%\package\Step-1_ANN_Two.py   %instance_root%\package\Step-1_ANN_Two.py  /Y
xcopy  %project_root%\package\Step-1_ANN_Two_Run_ProcessA.bat  %instance_root%\package\Step-1_ANN_Two_Run_ProcessA.bat  /Y
xcopy  %project_root%\package\Step-1_ANN_Two_Run_ProcessB.bat  %instance_root%\package\Step-1_ANN_Two_Run_ProcessB.bat  /Y
xcopy  %project_root%\package\Step-1_CombineCSV.py  %instance_root%\package\Step-1_CombineCSV.py  /Y
xcopy  %project_root%\package\Step-1_ANN_Two_CombineCSV_Run.bat  %instance_root%\package\Step-1_ANN_Two_CombineCSV_Run.bat  /Y
xcopy  %project_root%\package\Step-1_ANN_Two_SchtaskCreate.bat  %instance_root%\package\Step-1_ANN_Two_SchtaskCreate.bat  /Y
pause
