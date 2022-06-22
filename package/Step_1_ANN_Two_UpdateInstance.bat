cd ..\
set  project_root=%cd%
set  instance_root=D:\ANNTwo_CPU
echo Project root: %project_root%
echo instance_root root: %instance_root%
@REM data
xcopy  %project_root%\data\Step_0_ANN_Two_Result.csv  %instance_root%\data\Step_0_ANN_Two_Result.csv  /Y
xcopy  %project_root%\data\Step_0_ANN_Two_Result_ProcessA.csv  %instance_root%\data\Step_0_ANN_Two_Result_ProcessA.csv  /Y
xcopy  %project_root%\data\Step_0_ANN_Two_Result_ProcessB.csv  %instance_root%\data\Step_0_ANN_Two_Result_ProcessB.csv  /Y
xcopy  %project_root%\data\Step_0_ANN_Two_Result_ProcessC.csv  %instance_root%\data\Step_0_ANN_Two_Result_ProcessC.csv  /Y
xcopy  %project_root%\data\Step_0_ANN_Two_Result_ProcessD.csv  %instance_root%\data\Step_0_ANN_Two_Result_ProcessD.csv  /Y
xcopy  %project_root%\data\Step_0_ANN_Two_Result_ProcessE.csv  %instance_root%\data\Step_0_ANN_Two_Result_ProcessE.csv  /Y
xcopy  %project_root%\data\Step_1_Dataset.csv  %instance_root%\data\Step_1_Dataset.csv  /Y
@REM package
xcopy  %project_root%\package\Step_1_ANN_Two.py   %instance_root%\package\Step_1_ANN_Two.py  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_ModelDFIn.py   %instance_root%\package\Step_1_ANN_Two_ModelDFIn.py  /Y
xcopy  %project_root%\package\Step_0_WantedModel.py   %instance_root%\package\Step_0_WantedModel.py  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_Single.bat  %instance_root%\package\Step_1_ANN_Two_Run_Single.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_Double.bat  %instance_root%\package\Step_1_ANN_Two_Run_Double.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_Triple.bat  %instance_root%\package\Step_1_ANN_Two_Run_Triple.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_ModelDFIn_Run_Triple.bat  %instance_root%\package\Step_1_ANN_Two_ModelDFIn_Run_Triple.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_ProcessA.bat  %instance_root%\package\Step_1_ANN_Two_Run_ProcessA.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_ProcessB.bat  %instance_root%\package\Step_1_ANN_Two_Run_ProcessB.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_ProcessC.bat  %instance_root%\package\Step_1_ANN_Two_Run_ProcessC.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_ProcessD.bat  %instance_root%\package\Step_1_ANN_Two_Run_ProcessD.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_Run_ProcessE.bat  %instance_root%\package\Step_1_ANN_Two_Run_ProcessE.bat  /Y
xcopy  %project_root%\package\Step_1_CombineCSV.py  %instance_root%\package\Step_1_CombineCSV.py  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_CombineCSV_Run.bat  %instance_root%\package\Step_1_ANN_Two_CombineCSV_Run.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_SchtaskCreate.bat  %instance_root%\package\Step_1_ANN_Two_SchtaskCreate.bat  /Y
xcopy  %project_root%\package\Step_1_ANN_Two_SchtaskDelete.bat  %instance_root%\package\Step_1_ANN_Two_SchtaskDelete.bat  /Y
xcopy  %project_root%\package\Step_1_NewEnvBuild.py  %instance_root%\package\Step_1_NewEnvBuild.py  /Y
xcopy  %project_root%\package\Step_1_NewEnvBuild_Run.bat  %instance_root%\package\Step_1_NewEnvBuild_Run.bat  /Y






pause
