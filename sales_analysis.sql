use super_store_dataset;
-- Overall Performance
select sum(Sales) as Total_Sales,
		sum(Profit) as Total_Profit,
        (sum(Profit)/sum(Sales))*100 as Profit_Margin,
        Region
from `sample - superstore`;

-- Performance by Region
SELECT 
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    (SUM(Profit)/NULLIF(SUM(Sales),0))*100 AS Profit_Margin
FROM `sample - superstore`
group by Region
order by Profit_Margin desc;

-- Performance by Category
select sum(Sales) as Total_Sales,
		sum(Profit) as Total_Profit,
        (sum(Sales)/sum(Profit))*100 as Profit_Margin,
        Category
from `sample - superstore`
group by Category
order by Profit_Margin desc;

-- Top Customers 
select sum(Sales) as Total_Sales,
		sum(Profit) as Total_Profit,
        (sum(Sales)/sum(Profit))*100 as Profit_Margin,
        `Customer Name`
from `sample - superstore`
group by `Customer Name`
order by Total_Sales desc
limit 10;

-- Top Customers
select 
	year(str_to_date(`Order Date`, '%m/%d/%Y')) as sales_year,
	month(str_to_date(`Order Date`, '%m/%d/%Y')) as salesmonth,
	sum(Sales) as Total_Sales
from `sample - superstore`
group by 
	 YEAR(STR_TO_DATE(`Order Date`, '%m/%d/%Y')), 
    MONTH(STR_TO_DATE(`Order Date`, '%m/%d/%Y')) 
order by sales_year, salesmonth;

-- Loss-Making Customers
select sum(Sales) as Total_Sales,
		sum(Profit) as Total_Profit,
        (sum(Sales)/sum(Profit))*100 as Profit_Margin,
        `Customer Name`
from `sample - superstore`
group by `Customer Name`
having sum(Profit) < 0
order by Total_Profit desc;