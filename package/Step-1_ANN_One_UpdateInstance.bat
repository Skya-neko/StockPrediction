cd ..\
set  project_root=%cd%
set  instance_root=D:\ANNOne_CPU
echo Project root: %project_root%
echo instance_root root: %instance_root%
@REM xcopy /Y for "Yes replace the file"
@REM xcopy /I for "Do not ask me wether the new stuff is file or directory", but donsn't work on single file
@REM data
xcopy  %project_root%\data\Step-0_ANN_One_Result.csv  %instance_root%\data\Step-0_ANN_One_Result.csv  /Y
xcopy  %project_root%\data\Step-0_ANN_One_Result_ProcessA.csv  %instance_root%\data\Step-0_ANN_One_Result_ProcessA.csv  /Y
xcopy  %project_root%\data\Step-0_ANN_One_Result_ProcessB.csv  %instance_root%\data\Step-0_ANN_One_Result_ProcessB.csv  /Y
xcopy  %project_root%\data\Step-1_Dataset.csv  %instance_root%\data\Step-1_Dataset.csv  /Y
xcopy  %project_root%\data\Step-1_ANN_One_Scaler.gz  %instance_root%\data\Step-1_ANN_One_Scaler.gz  /Y

@REM package
xcopy  %project_root%\package\Step-1_ANN_One.py   %instance_root%\package\Step-1_ANN_One.py  /Y
xcopy  %project_root%\package\Step-1_ANN_One_Run_ProcessA.bat  %instance_root%\package\Step-1_ANN_One_Run_ProcessA.bat  /Y
xcopy  %project_root%\package\Step-1_ANN_One_Run_ProcessB.bat  %instance_root%\package\Step-1_ANN_One_Run_ProcessB.bat  /Y
xcopy  %project_root%\package\Step-1_CombineCSV.py  %instance_root%\package\Step-1_CombineCSV.py  /Y
xcopy  %project_root%\package\Step-1_ANN_One_CombineCSV_Run.bat  %instance_root%\package\Step-1_ANN_One_CombineCSV_Run.bat  /Y
xcopy  %project_root%\package\Step-1_ANN_One_SchtaskCreate.bat  %instance_root%\package\Step-1_ANN_One_SchtaskCreate.bat  /Y
pause
