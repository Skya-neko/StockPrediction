# ANN_Two-SQL-Syntax

## Find best model

```sql=
DECLARE @rmseLimit AS int
SET @rmseLimit = 15

DECLARE @countDuration AS int
SET @countDuration = 25


-- The purpose is to find best model, but this also can find model has how many durations satiesfied limit.
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
--INTO #countLimit --drop table #countLimit
FROM [traing_result].[dbo].[Step_0_ANN_Two_Result_20220620]
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
```

## data Observation
```sql=

-- This is for data observation like, what is the best result now?
-- Although it is not smaller than the rmse limit we want, but we can see which model is closer to the best result.

-- Remove model has unsatisfied rmse during any duration
SELECT D.*
INTO #allInLimit
From(
	-- SELECT any duration which is exceed rmse limit in models 
	SELECT B.*
	FROM #countLimit A
	INNER JOIN [Step_0_ANN_Two_Result_20220620] B
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
	AND rmse > 50
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
```

## Best model until now
```sql=
SELECT *
FROM [traing_result].[dbo].[ANN_Two_Result]
WHERE [random_seed] = 90
AND [Dense1Units] = 7
AND [Dense2Units] = 22
AND [learning_rate] = 0.000001
AND [epochs] = 4000
ORDER BY startDate
```
keras_5_52191.h5,30.49,5.52,103.46,2022/06/23 18:00:17,2021-05-24,2021-06-07,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_9_79392.h5,95.92,9.79,104.28,2022/06/23 18:02:06,2021-06-07,2021-06-22,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_7_26816.h5,52.83,7.27,101.98,2022/06/23 18:03:53,2021-06-22,2021-07-06,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_11_4037.h5,130.05,11.4,102.78,2022/06/23 18:05:40,2021-07-06,2021-07-20,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_5_67773.h5,32.24,5.68,103.26,2022/06/23 18:07:28,2021-07-20,2021-08-03,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_4_06035.h5,16.49,4.06,103.25,2022/06/23 18:09:16,2021-08-03,2021-08-17,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_9_73492.h5,94.77,9.73,106.39,2022/06/23 18:11:07,2021-08-17,2021-08-31,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_7_42766.h5,55.17,7.43,107.17,2022/06/23 18:12:59,2021-08-31,2021-09-14,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_8_64501.h5,74.74,8.65,111.02,2022/06/23 18:14:55,2021-09-14,2021-09-30,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_7_93814.h5,63.01,7.94,118.45,2022/06/23 18:16:58,2021-09-30,2021-10-17,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple
keras_5_51616.h5,30.43,5.52,111.43,2022/06/23 18:18:55,2021-10-17,2021-10-31,41,148,41,1e-06,0,0.9,True,sgd,mean_squared_error,2000,0,10,Vivian,Triple