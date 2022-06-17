cd ../
set  project_root=%cd%
set  instance_root=D:\ANNTwo_CPU
echo Project root: %project_root%
echo instance_root root: %instance_root%
@REM data
xcopy  %project_root%/data/Step-0_ANNTwoResult.csv  %instance_root%/data/Step-0_ANNTwoResult.csv
xcopy  %project_root%/data/Step-0_ANNTwoResult_ProcessA.csv  %instance_root%/data/Step-0_ANNTwoResult_ProcessA.csv
xcopy  %project_root%/data/Step-0_ANNTwoResult_ProcessB.csv  %instance_root%/data/Step-0_ANNTwoResult_ProcessB.csv
xcopy  %project_root%/data/Step-1_Dataset.csv  %instance_root%/data/Step-1_Dataset.csv
@REM package
xcopy  %project_root%/package/Step-1_ANN_Two.py   %instance_root%/package/Step-1_ANN_Two.py
xcopy  %project_root%/package/Step-1_ANN_Two_Run_ProcessA.bat  %instance_root%/package/Step-1_ANN_Two_Run_ProcessA.bat
xcopy  %project_root%/package/Step-1_ANN_Two_Run_ProcessB.bat  %instance_root%/package/Step-1_ANN_Two_Run_ProcessB.bat
xcopy  %project_root%/package/Step-1_CombineCSV.py  %instance_root%/package/Step-1_CombineCSV.py
xcopy  %project_root%/package/Step-1_CombineCSV_Run.bat  %instance_root%/package/Step-1_CombineCSV_Run.bat
xcopy  %project_root%/package/Step-1_SchtaskCreate.bat  %instance_root%/package/Step-1_SchtaskCreate.bat
