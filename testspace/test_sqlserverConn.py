from pymssql import connect
from sqlalchemy import create_engine
import pandas as pd
server = 'localhost'  # DESKTOP-2LNIJAK\SQLEXPRESS'  :57226
username = r'DESKTOP-2LNIJAK\Vivian'
password = '60130327'
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
engine = create_engine(conn_str)
conn = engine.connect()

# sqlalchemy application
# res = conn.execute("SELECT * FROM dbo.[Step-0_ANN_Two_Result_20220619]")
# for row in res:
#     print(row)
# conn.close()



print('pandas!')
# pandas & sqlalchemy application
# table = pd.read_sql('Step-0_ANN_Two_Result_20220619', con=engine)

recordDF = pd.read_csv('./data/Step-0_ANN_Two_Result.csv',index_col=False)
recordDF.to_sql('Step-0_ANN_Two_Result_20220620', con=engine)

