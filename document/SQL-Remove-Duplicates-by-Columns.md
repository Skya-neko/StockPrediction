# SQL-Remove-Duplicates-by-Columns
## Remove duplicates without primary key
```sql=
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (10) *
INTO #original_table  
FROM [traing_result].[dbo].[ANN_Two_Result_No_Machine]
UNION ALL
SELECT TOP (10) *
FROM [traing_result].[dbo].[ANN_Two_Result_No_Machine]


SELECT *
INTO #remove_duplicates_target
FROM #original_table


WITH cte AS (
    SELECT *, 
		ROW_NUMBER() OVER (
			PARTITION BY 
				[startDate]
				,[endDate]
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
            ORDER BY 
				[startDate]
				,[endDate]
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
		) RowNumber
    FROM #remove_duplicates_target
)
DELETE
FROM cte
WHERE RowNumber > 1;


-- Compare #remove_duplicates_target with #original_table
SELECT *
FROM #original_table

SELECT *
FROM #remove_duplicates_target


```

我不想要在python端用insert資料的方式insert新資料到SQL(整個表的都是新的還要用insert into 語句迭代，比較麻煩點也比較慢)。所以使用整表更新，也就是在to_sql的時候做一次性資料寫入SQL table`ANN_Two_Result_{machine}`，再由另一個Job去把多個machine的資料表匯入`ANN_Two_Result`後並去重。也許有方法使用組合鍵作為primary key達到去重的方法，但由於我先查到這個方便的方法(不用primary key的髒做法)，所以先替用一下XD。


cte全名為common table expression，其實直接當作一個子查詢就好了，特別的是直接```DELETE FROM cte WHERE ......```就可以直接改變原始表(子查詢的來源表)。因此執行這整個程式碼後可以看到`#remove_duplicates_target`直接被改變。


`WITH cte AS (子查詢內容)`括號中放置的就是子查詢的內容，子查詢的內容把它單獨SELECT出來會更清楚：
```sql=
SELECT *, ROW_NUMBER() OVER (
	PARTITION BY 
		[startDate]
		,[endDate]
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
	ORDER BY 
		[startDate]
		,[endDate]
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
	) RowNumber
FROM #original_table
```
子查詢的SELECT中先是SELECT了所有欄位的內容，再SELECT了一個由`ROW_NUMBER() OVER(計算條件)`產生的欄位`RowNumber`，當中的計算欄位使用`PARTITION BY`的用意像是下圖：
![](https://i.imgur.com/QQJbk4T.png)
將擁有同樣欄位值的資料分區，在每一區編號每一列。
> The function 'ROW_NUMBER' must have an OVER clause with ORDER BY


最後，神奇的是，利用cte這個暫時具名的表刪除`RowNumber`大於1的列後，`RowNumber`也自然的消失了。可能這就是cte的作用吧，用cte暫時具名表的條件更改原始表。
