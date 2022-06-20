# Guide-SQL-Query-With-Python
## Configuration
```python=
server = 'localhost'  # DESKTOP-2LNIJAK\MSSQLSERVER
username = r'DESKTOP-2LNIJAK\Vivian'
password = ''
database_name = 'traing_result'
port = 1433
```
我的MSSQL有兩種Server:
1. MSSQLSERVER
2. SQLEXPRESS

我選擇MSSQLSERVER這台Server
![](https://i.imgur.com/G2fodvR.png)
點進MSSQLSERVER的通訊協定就可以得到server和port資訊

Username則是從SSMS-->connected server(DESKTOP-2LNIJAK)-->Security-->Logins看到目前有哪些帳戶可以access DESKTOP-2LNIJAK


## pymssql
```python=
from pymssql import connect

# pymssql connection
server_args = {'server': server, 'user': username, 'password': password,
               'database': database_name, 'port': port, 'charset': 'UTF-8'}
conn = connect(**server_args)
cursor = conn.cursor(as_dict=True)  # as_dict=True make sql return row data which data type is dictionary

# pymssql application
cursor.execute("SELECT * FROM dbo.[Step-0_ANN_Two_Result_20220619]")
for row in cursor:
    print(row)

cursor.close()
conn.close()
```

## sqlalchemy
```python=
# sqlalchemy connection
conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}'


# Engine held globally for the lifetime of a single application process.
# A single Engine manages many individual DBAPI connections on behalf of the process,
# and is intended to be called upon in a concurrent fashion.
engine = create_engine(conn_str)
conn = engine.connect()  # new a DBAPI instance, it is equal to a Query Page in SQL Server
conn2 = engine.connect()  # new another DBAPI instance, it is equal to a Query Page in SQL Server

# sqlalchemy application - SELECT
SQLReturn = conn.execute("SELECT * FROM dbo.[Step-0_ANN_Two_Result_20220619]")
for row in SQLReturn:
    print(row)
conn.close()

# sqlalchemy application - SELECT INTO #TEMP
# Correct example
SQLReturn = conn.execute("SELECT * INTO #TEMP FROM dbo.[Step-0_ANN_Two_Result_20220619]")  # Create #TEMP return is None
SQLReturn = conn.execute("SELECT * FROM #TEMP")
# Incorrect example: showing that each DBAPI is independant:
SQLReturn = conn.execute("SELECT * INTO #TEMP FROM dbo.[Step-0_ANN_Two_Result_20220619]")
SQLReturn = conn2.execute("SELECT * FROM #TEMP")

# sqlalchemy application - INSERT INTO
trans = conn.begin()
try:
    conn.execute("INSERT INTO films VALUES ('Comedy', '82 minutes');")
    conn.execute("INSERT INTO datalog VALUES ('added a comedy');")
    trans.commit()
except:
    trans.rollback()
    raise
```
[create_engine() official doc](https://docs.sqlalchemy.org/en/13/core/connections.html)
可以從內容推斷，DBAPI就是指new一個engine.connect()!


## pandas & sqlalchemy application
[what is SET NOCOUNT ON 實作畫面](https://ithelp.ithome.com.tw/articles/10198514)
[what is SET NOCOUNT ON 用作 multiple query 且只回傳最後的SELECT結果](https://stackoverflow.com/questions/49516278/python-running-sql-query-with-temp-tables)
> the pandas read_sql method can only support one result set. However, when you generate a temp table in T-sql you do create a result set in the form "(XX row(s) affected)" which is what causes your original query to fail. By setting NOCOUNT you eliminate any early returns and only get the results from your final SELECT statement.

```python=

# pandas & sqlalchemy application
# pd.read_sql:　can read both of the table name or the query command.
table = pd.read_sql('Step-0_ANN_Two_Result_20220619', con=engine)
table = pd.read_sql('SELECT TOP 10 FROM Step-0_ANN_Two_Result_20220619', con=engine)

# Save DataFrame to sql
recordDF = pd.read_csv('./data/Step-0_ANN_Two_Result.csv',index_col=False)
recordDF.to_sql('Step-0_ANN_Two_Result_20220620', con=engine)


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
```