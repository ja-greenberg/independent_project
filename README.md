# Retail Data Analysis Project
Author: Jack Greenberg

This project focuses on preparing and analyzing two retail datasets using Python and pandas:
- Walmart sales data
- Amazon product and review data

The first stage of the project involved cleaning and validating both datasets so they could be used reliably for analysis. I have two separate retail datasets because I was interested in both of them. I currently do not have plans to compare the two datasets.

The second stage focused on exploratory data analysis through visualizations. For the Walmart dataset, I built seven graphs to understand broad sales patterns, seasonality, and economic relationships across all 45 stores in the data. My big takeaway from this was that chain-wide factors don't explain much, and I need to focus on the individual store level.

The third stage I finished a chain-wide exploration and switched focus to store level data comparing the top 10 and bottom 10 performing stores by total sales ($). I ran two LR models on the economic factors and time based factors in regression.py which both performed horribly, confirming that there isn't much to gain from looking at the data on the chain level. Decided I want to focus this analysis around the question, "What separates Walmart's best stores from its worst, and can I predict it.". The top performing stores were almost all Type A, and the bottom 10 are mostly Type B and C. But when I normalized sales by store size to look at sales per square foot, Type B and C were leading ahead of A. So Type A stores sell more in raw dollars, but types B and C are more efficient, selling more per square foot. This split my analysis into looking at how different predictors affect raw sales, and sales per square foot. I left off by comparing holiday vs non-holiday sales for both groups. Top 10 stores all, as expected, see a positive bump and lower ranked stores are inconsistent. But more importantly the holiday rankings mirror the overall rankings almost exactly, meaning holidays amplify existing performance rather than changing it.

## Current Focus
- Walmart:
    Run linear regression on the economic features and the time based features to test how well those variables predict sales. 
    Store level analysis on why the top 10 and bottom 10 stores perform so differently. 

Amazon:

## Objectives
- Walmart:
    Answer the question, "What separates Walmart's best stores from its worst, and can we predict it?"
    
- Decide whether to focus on one dataset and abandon the other, create two separate case studies, or analyze them separately while creating a broader story about different aspects of retail

## Completed Objectives
- Clean the data
- Explore walmart dataset

## Datasets

### Walmart Dataset
walmart_clean.csv contains date-based weekly sales data.
stores.csv contains store #, Type, Size, Avg_Weekly_Sales, Sales_per_SqFt

### Amazon Dataset
The Amazon dataset contains product, category, pricing, discount, rating, and review-related fields.

