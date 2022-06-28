from sqlalchemy import create_engine
from sqlalchemy.types import *
import pandas as pd
from datetime import datetime

def write_log(something):
    print(f"INFO - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - ", something)


server = '140.134.25.164'  # DESKTOP-2LNIJAK\SQLEXPRESS'  :57226
username = r'Vivian'  #DESKTOP-2LNIJAK\Vivian
password = 'L102210221022'
database_name = 'traing_result'
port = 1433
fromTable = 'ANN_Two_Result'

conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}'
engine = create_engine(conn_str)
# conn = engine.connect()

resultDF = pd.read_sql(fromTable, con=engine)
resultDF.to_csv(f"{fromTable}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv", encoding='big5', index=False)
write_log('End - Download results from SQL.')

