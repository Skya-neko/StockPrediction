"""
When build training job in new environment,
change the project root path in new environmnet and change var machine to specify which machine is going to run.
"""
import os
import sys
protjectRoot = sys.argv[1]  # D:\ANNTwo_CPU
machine = sys.argv[2]  # Vivian

fileNameList = os.listdir(protjectRoot+ r'\package')
replaceTarget = r'D:\StockPrediction\StockPrediction'

for fileName in fileNameList:
    with open(protjectRoot+r'\package\\'+fileName, mode='r', encoding='utf8') as fileIn:
        content = fileIn.read()
        content = content.replace(replaceTarget, protjectRoot)
        with open(protjectRoot + r'\package\\' + fileName, mode='w', encoding='utf8') as fileOut:
            fileOut.write(content)

with open(protjectRoot+r'\package\Step_1_ANN_Two.py', mode='r', encoding='utf8') as file:
    content = file.read()
    content = content.replace("machine = 'Vivian'", f"machine = '{machine}'")
    with open(protjectRoot+r'\package\Step_1_ANN_Two.py', mode='w', encoding='utf8') as fileOut:
        fileOut.write(content)
