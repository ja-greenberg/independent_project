**vis1: Total weekly sales over time line chart**

The two most prominent sale spikes each year occur around Thanksgiving/Black Friday and Christmas, with the late November week consistently producing the highest sales across the entire dataset peaking near $80M in 2011. Outside of those holiday surges, weekly sales remain relatively flat in the $40M-$50M range, suggesting that overall demand is stable and the big swings are almost entirely holiday-driven. Super Bowl and Labor Day weeks show little visible impact compared to the year-end holidays.


**vis2: Average sales by month bar chart**

December is the peak month with \~1.3M average in weekly sales. Closely followed by November with \~1.15M. Both of these months are driven by the holiday season. The remaining months clusers between 0.9M and 1.10M, with January being the weakest month by far, which I am guessing is people watching their wallets after holiday spending. June was the third highest which may point to spending in preparation for summer, or summer vacations. But it isn't ahead of the pack by much so I'm taking it with a grain of salt.


**vis3: Holiday vs non holiday weeks bar chart**

Holiday weeks average $1.12M in sales per store compared to $1.04M for non-holiday weeks, a difference of roughly $80,000 per store. While holiday weeks make up only 10 out of \~143 calendar weeks in the dataset, they consistently drive higher spending. Scaled across all 45 stores, each holiday week generates approximately $3.6M more than a typical week.


**vis4: top and bottom 10 stores bar chart**

Store earnings vary dramatically across the data. The top performing store (20), averages over $2M in weekly sales, while the lowest (33) barely reaches $0.25M. The top 10 cluster between $1.2M and $2.2M while the bottom 10 all fall below $0.75M. Further study required on why the top and bottom stores are performing so differently.


**vis5: Correlation heatmap**

Weekly sales didn't correlate strongly with anything. The highest weekly sales correlation was unemployment, suggesting higher unemployment was weakly (heh) associated with lower sales, but still not much there to look at. The most notable relationships were fuel price \& year, CPI \& unemployment, and unemployment and year. Overall, not much to go on here and the majorly weak correlations here tell me linear regression alone will have a hard time explaining / predicting sales variation. This finding aligns with the top and bottom 10 stores chart where contributors unique to each store will be more important than a broad chain-wide view.


**vis6: Sales vs economic indicators scatters**

All four scatter plots reinforce the heatmap findings. Trend lines are nearly flat across the board, confirming weak relationships between broad chain-wide sales numbers and the economic indicators in the data. CPI and Unemployment show visible clustering, further emphasizing individual store-level groupings. Temperature and Fuel Price show more even distributions with no clear pattern. Overall, these plots reinforce that economic conditions at the chain-wide level do not drive individual store sales.


**vis7: Year-over-year comparison line chart**

All three years show extremely similar patterns. We see spikes at the expected time periods, supporting the findings in vis1. We see possible minor year-over-year growth in 2012 but nothing substantial. Unfortunately, the data cuts off in Oct 2012 so we don't get to see the final year's holiday season. Not a ton to be gained here.

