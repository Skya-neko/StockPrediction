from sqlalchemy import create_engine
import pandas as pd
server = '140.134.25.164'  # localhost # DESKTOP-2LNIJAK\SQLEXPRESS'
username = r'Vivian'  #DESKTOP-2LNIJAK\Vivian
password = 'L102210221022'
database_name = 'traing_result'
port = 1433



conn_str = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database_name}'
engine = create_engine(conn_str)
conn = engine.connect()

def best_modelDF(table, limitRMSE):
    # Exactly best model for the limitRMSE
    queryCMD = f"""
    DECLARE @rmseLimit AS int
    SET @rmseLimit = {limitRMSE}
    
    DECLARE @countDuration AS int
    SET @countDuration = 25
    
    -- The purpose is to find best model, but this also can find model has how many durations satiesfied limitRMSE.
    -- Prediction preiod has 25 predicted duration, thus if a model count(*)=25 then we find the best model.
    SELECT COUNT(*) AS [count]
        ,[random_seed]
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
    FROM [traing_result].[dbo].[{table}]
    WHERE rmse < @rmseLimit
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
    HAVING COUNT(*) >= @countDuration  --If COUNT(*) = 25 than find the best model.
    """

    try:
        return pd.read_sql(queryCMD, con=engine)
    except:
        return None

def observed_modelDF(table, limitRMSE, countDuration, endureRMSE):
    queryCMD = f"""
    SET NOCOUNT ON
    
    
    DECLARE @rmseLimit AS int
    SET @rmseLimit = {limitRMSE}
    
    DECLARE @countDuration AS int
    SET @countDuration = {countDuration}  -- At least n records satiesfy the limitRMSE
    
    -- The purpose is to find best model, but this also can find model has how many durations satiesfied limitRMSE.
    -- Prediction preiod has 25 predicted duration, thus if a model count(*)=25 then we find the best model.
    SELECT COUNT(*) AS [count]
        ,[random_seed]
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
    INTO #countLimit --drop table #countLimit
    FROM [traing_result].[dbo].[{table}]
    WHERE rmse < @rmseLimit
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
    HAVING COUNT(*) > @countDuration  --If COUNT(*) = 25 than find the best model.
    
    
    -- This is for data observation like, what is the best result now?
    -- Although it is not smaller than the rmse limitRMSE we want, but we can see which model is closer to the best result.
    
    -- Remove model has unsatisfied rmse during any duration
    SELECT D.*
    From(
        -- SELECT any duration which is exceed endureRMSE in models 
        SELECT B.*
        FROM #countLimit A
        INNER JOIN [{table}] B
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
        WHERE A.[random_seed] = B.[random_seed]
        AND rmse > {endureRMSE}
        --ORDER BY [Dense1Units], [Dense2Units], startDate ASC
    ) C
    RIGHT JOIN #countLimit D
    ON  C.[random_seed] = D.[random_seed]
    AND C.[Dense1Units] = D.[Dense1Units]
    AND C.[Dense2Units] = D.[Dense2Units]
    AND C.[learning_rate] = D.[learning_rate]
    AND C.[decay] = D.[decay]
    AND C.[momentum] = D.[momentum]
    AND C.[nesterov] = D.[nesterov]
    AND C.[optimizer] = D.[optimizer]
    AND C.[loss] = D.[loss]
    AND C.[epochs] = D.[epochs]
    AND C.[verbose] = D.[verbose]
    AND C.[batch_size] = D.[batch_size]
    WHERE C.[random_seed] IS NULL
    """
    # print(queryCMD)
    try:
        return pd.read_sql(queryCMD, con=engine)
    except :
        return None

if __name__ == '__main__':
    table = 'ANN_Two_Result'
    limitRMSE = 15
    countDuration = 23  # At least n records satiesfy the limitRMSE
    endureRMSE = 19  # 17.7  # 50
    bestDF = best_modelDF(table, limitRMSE)
    observedDF = observed_modelDF(table, limitRMSE, countDuration, endureRMSE)
