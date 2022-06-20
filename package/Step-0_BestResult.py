from pymssql import connect
from sqlalchemy import create_engine
import pandas as pd
server = 'localhost'  # DESKTOP-2LNIJAK\SQLEXPRESS'  :57226
username = r'DESKTOP-2LNIJAK\Vivian'
password = '60130327'
database_name = 'traing_result'
port = 1433


# sqlalchemy connection
conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}'
engine = create_engine(conn_str)
conn = engine.connect()
queryCMD = """

SELECT DISTINCT [random_seed]
      ,[Dense1Units]
      ,[Dense2Units]
      ,[learning_rate]
      ,[decay]
      ,[momentum]
      ,[nesterov]
      ,[optimizer]
      ,[loss]
      ,[epochs]
      ,[verbose]
      ,[batch_size]
INTO #beyond   
FROM [traing_result].[dbo].[Step-0_ANN_Two_Result_20220619]
WHERE rmse > 15
"""
SQLReturn = conn.execute(queryCMD)

queryCMD = """

SELECT B.*
INTO #satiesfiedLimit
FROM #beyond A --drop table #beyond
RIGHT JOIN [Step-0_ANN_Two_Result_20220619] B
ON  A.[random_seed] = B.[random_seed]
AND A.[Dense1Units] = B.[Dense1Units]
AND A.[Dense2Units] = B.[Dense2Units]
AND A.[learning_rate] = B.[learning_rate]
AND A.[decay] = B.[decay]
AND A.[momentum] = B.[momentum]
AND A.[nesterov] = B.[nesterov]
AND A.[optimizer] = B.[optimizer]
AND A.[loss] = B.[loss]
AND A.[epochs] = B.[epochs]
AND A.[verbose] = B.[verbose]
AND A.[batch_size] = B.[batch_size]
WHERE A.[random_seed] IS NULL

"""
SQLReturn = conn.execute(queryCMD)


queryCMD = """

SELECT [random_seed]
      ,[Dense1Units]
      ,[Dense2Units]
      ,[learning_rate]
      ,[decay]
      ,[momentum]
      ,[nesterov]
      ,[optimizer]
      ,[loss]
      ,[epochs]
      ,[verbose]
      ,[batch_size]
INTO #modelResult
FROM #satiesfiedLimit
GROUP BY [random_seed]
      ,[Dense1Units]
      ,[Dense2Units]
      ,[learning_rate]
      ,[decay]
      ,[momentum]
      ,[nesterov]
      ,[optimizer]
      ,[loss]
      ,[epochs]
      ,[verbose]
      ,[batch_size]
HAVING count(*) > 1
"""

# conn.close()



print('pandas!')
# pandas & sqlalchemy application
recordDF = pd.read_sql('Step-0_ANN_Two_Result_20220620', con=engine)

queryCMD = """
SELECT DISTINCT
       [random_seed]
      ,[Dense1Units]
      ,[Dense2Units]
      ,[learning_rate]
      ,[decay]
      ,[momentum]
      ,[nesterov]
      ,[optimizer]
      ,[loss]
      ,[epochs]
      ,[verbose]
      ,[batch_size]
FROM [traing_result].[dbo].[Step-0_ANN_Two_Result_20220620]
"""
modelDF = pd.read_sql_query(queryCMD, con=engine)
for i in range(len(modelDF)):

    recordDF.isin()