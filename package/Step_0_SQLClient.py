from pymssql import connect
from sqlalchemy import create_engine
import pandas as pd
server = '140.134.25.164'  # DESKTOP-2LNIJAK\MSSQLSERVER
username = r'Vivian'
password = 'L102210221022'
database_name = 'traing_result'
port = 1433

# sqlalchemy connection
conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}'
engine = create_engine(conn_str)
conn = engine.connect()  # new a DBAPI instance, it is equal to a Query Page in SQL Server

recordDF = pd.read_sql("SELECT * FROM ANN_Two_Result", con=engine)
print(recordDF.head(10))