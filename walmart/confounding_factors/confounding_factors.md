**1 CPI & Unemployment:**

CPI varies by an average of only 3.12 within a single store over 2.5 years, but the standard deviation between store means is 39.66 -- a 12x difference. This means CPI barely changes over time at any individual store but differs dramatically between stores. The visualization confirms this with stores clustering into distinct horizontal bands. CPI is therefore not measuring inflation effects on sales; it is acting as a regional identifier. Unemployment shows the same pattern with a 3x ratio between within-store and between-store variation. When earlier regression models suggested "higher CPI lowers sales," they were really capturing the fact that smaller stores tend to be located in higher-CPI regions.


**2 Size & Type:**

Type and Size carry overlapping information. Type C stores are nearly identical in size (39K-43K sqft), while Type A averages 177K sqft and Type B averages 101K sqft. The correlation between type (as 0/1/2) and size is -0.786, indicating they move together strongly. Including both in a model is redundant because once you know a store's type, you can predict its size with high accuracy. Including them as separate features would double-count the same underlying variable -- store scale.


**3 Fuel price & Year:**

Fuel price and year carry overlapping information. Average fuel prices rose from $2.82 in 2010 to $3.71 in 2012, with a correlation of 0.779 between fuel price and year. This means fuel price isn't capturing an independent economic effect on sales; it's largely tracking the passage of time during a period of rising costs. A regression model can't distinguish whether changes in sales are driven by fuel prices or by year-over-year trends because they move together so closely. Including both is redundant.


**4 Month & Year:**

Month and week carry essentially the same information, with a correlation of 1.00 in the original heatmap. Both encode position within the calendar year, so including both in a model adds no new information. This is the cleanest case of redundancy in the dataset and the easiest to drop in any future modeling.