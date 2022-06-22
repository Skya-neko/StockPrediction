from newegg_ConnInstance import ConnInstance
userName = 'etl_sp'
ServerName = 'E11BIDB04'
DBName = 'ETLSchedule'
Instance = ConnInstance.ConnInstance()
engine = Instance.get_connection('sqlalchemy', userName, ServerName, DBName)
conn = engine.connect(close_with_result=True)
QueryCMD = ''' SELECT TOP 3 * FROM F_2021_ETLRelatedTableList WITH(NOLOCK) '''
result = conn.execute(QueryCMD)
for row in result:
    print(row)
    result.close()