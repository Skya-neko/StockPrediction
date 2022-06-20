from pymssql import connect
from sqlalchemy import create_engine
import pandas as pd
server = 'localhost'  # DESKTOP-2LNIJAK\MSSQLSERVER
username = r'Vivian'
password = 'L102210221022'
database_name = 'traing_result'
port = 1433

# # pymssql connection
# server_args = {'server': server, 'user': username, 'password': password,
#                'database': database_name, 'port': port, 'charset': 'UTF-8'}
# conn = connect(**server_args)
# cursor = conn.cursor(as_dict=True)  # as_dict=True make sql return row data which data type is dictionary

# pymssql application
# cursor.execute("SELECT * FROM dbo.[Step-0_ANN_Two_Result_20220619]")
# for row in cursor:
#     print(row)
#
# cursor.close()
# conn.close()




# sqlalchemy connection
conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}'
# Engine held globally for the lifetime of a single application process.
# A single Engine manages many individual DBAPI connections on behalf of the process,
# and is intended to be called upon in a concurrent fashion.
engine = create_engine(conn_str)
conn = engine.connect()  # new a DBAPI instance, it is equal to a Query Page in SQL Server
conn2 = engine.connect()  # new another DBAPI instance, it is equal to a Query Page in SQL Server

# sqlalchemy application - SELECT
# SQLReturn = conn.execute("SELECT * FROM dbo.[Step-0_ANN_Two_Result_20220619]")
# for row in SQLReturn:
#     print(row)
# conn.close()

# sqlalchemy application - SELECT INTO #TEMP
# Correct example
SQLReturn = conn.execute("SELECT * INTO #TEMP FROM dbo.[Step-0_ANN_Two_Result_20220619]")  # Create #TEMP return is None
SQLReturn = conn.execute("SELECT * FROM #TEMP")
# Incorrect example: showing that each DBAPI is independant:
# SQLReturn = conn.execute("SELECT * INTO #TEMP FROM dbo.[Step-0_ANN_Two_Result_20220619]")
# SQLReturn = conn2.execute("SELECT * FROM #TEMP")

# sqlalchemy application - INSERT INTO
trans = conn.begin()
try:
    conn.execute("INSERT INTO films VALUES ('Comedy', '82 minutes');")
    conn.execute("INSERT INTO datalog VALUES ('added a comedy');")
    trans.commit()
except:
    trans.rollback()
    raise




# pandas & sqlalchemy application
# pd.read_sql:　can read both of the table name or the query command.
# table = pd.read_sql('Step-0_ANN_Two_Result_20220619', con=engine)
# table = pd.read_sql('SELECT TOP 10 FROM Step-0_ANN_Two_Result_20220619', con=engine)

# Save DataFrame to sql
# recordDF = pd.read_csv('./data/Step-0_ANN_Two_Result.csv',index_col=False)
# recordDF.to_sql('Step-0_ANN_Two_Result_20220620', con=engine)


# Mark that each of the pd.read_sql will new a DBAPI instance.
# Correct example
# "SET NOCOUNT ON" refer to no return from sql server, thus we can put multiple query into pd.read_sql
queryCMD = """
SET NOCOUNT ON
SELECT * INTO #TEMP FROM dbo.[Step-0_ANN_Two_Result_20220619]
SELECT * FROM #TEMP
"""
recordDF = pd.read_sql("SELECT * FROM #TEMP", con=engine)
# Incorrect example
recordDF = pd.read_sql("SELECT * INTO #TEMP FROM dbo.[Step-0_ANN_Two_Result_20220619]", con=engine)  # Create #TEMP return is None
recordDF = pd.read_sql("SELECT * FROM #TEMP", con=engine)