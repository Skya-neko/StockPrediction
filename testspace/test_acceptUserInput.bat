cd ../
set  project_root=%cd%
echo Project root: %project_root%
echo Your project root is: %project_root%
set /p machine=Enter computer name (e.g. Clinton):
echo Your computer name is: %machine%
python   %project_root%\package\Step_1_NewEnvBuild.py  %project_root%  %machine%
pause
