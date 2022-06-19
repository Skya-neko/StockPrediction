SET "today=%date:~0,10%"
python   .\package\Step-1_ANN_Two.py Step-0_ANN_Two_Result_ProcessE.csv Double >>   .\log\Log-ANN_Two_Result_ProcessE_%today:/=-%.txt  2>&1
pause :: Keep the window open
@REM %today:/=-% Means replace "/" with "-"