"""
When build training job in new environment,
change the project root path in new environmnet.
"""
import os
import sys
protjectRoot = sys.argv[1]  # D:\ANNTwo_CPU

fileNameList = os.listdir(protjectRoot+ r'\package')
replaceTarget = r'D:\StockPrediction\StockPrediction'

for fileName in fileNameList:
    with open(protjectRoot+r'\package\\'+fileName, mode='r', encoding='utf8') as fileIn:
        content = fileIn.read()
        content = content.replace(replaceTarget, protjectRoot)
        with open(protjectRoot + r'\package\\' + fileName, mode='w', encoding='utf8') as fileOut:
            fileOut.write(content)

