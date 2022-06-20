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
FROM [traing_result].[dbo].[Step-0_ANN_Two_Result_20220620]
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
	INNER JOIN [Step-0_ANN_Two_Result_20220620] B
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