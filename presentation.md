Title Slide:
Walmart Store Performance: A Data-Driven Analysis
    What separates Walmart's best stores from its worst, and can we predict it?


The Data:
    45 Walmart stores across the US
    Weekly sales data from February 2010 to October 2012
    6,435 total rows (one per store, per week)
    Includes economic indicators: temperature, fuel price, CPI, unemployment
    Holiday flag for major retail weeks (Super Bowl, Labor Day, Thanksgiving, Christmas)
    Supplemental data on store type (A, B, C) and square footage

    This data was sourced from Kaggle. It contains sales data for 45 Walmart stores located in different regions. The data is split into two datasets: Walmart.csv which contains Store, Date, Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, and Unemployment. When cleaning I added Year, Month, and Week for analysis. The second dataset is Stores.csv which contains Store, Type, and Size, and I added Avg_Weekly_Sales and Sales_per_SqFt for analysis. The two datasets were later merged in store_analysis.py. The Kaggle page also specifies four holidays whose dates were provided ahead of time:
        Super Bowl: 12-Feb-10, 11-Feb-11, 10-Feb-12
        Labor Day: 10-Sep-10, 9-Sep-11, 7-Sep-12
        Thanksgiving: 26-Nov-10, 25-Nov-11, 23-Nov-12
        Christmas: 31-Dec-10, 30-Dec-11, 28-Dec-12


Research Question:
    What separates Walmart's best stores from its worst, and can we predict it? This question came out of the chain-wide exploration. The gap between the top performing and bottom performing stores was dramatic, with an 8:1 ratio in average weekly sales. That gap became the most interesting thing in the dataset, so the project pivoted to focus on identifying what structural and operational differences drive that performance gap. I looked at performance through two lenses: total weekly sales in raw dollars, and sales per square foot to measure efficiency. The goal is to understand what separates the best stores from the worst across both metrics, and whether those differences are predictable from the data available.


Chain-wide EDA:
    Total Weekly Sales Over Time:
        The first thing I looked at was overall sales over the 2.5 year window. Two patterns stood out. Sales are flat for most of the year, hovering around $45 million to $50 million chain-wide. The dramatic spikes come from Thanksgiving and Christmas, where sales jump to $70-80 million. Super Bowl and Labor Day are also flagged as holidays in the data but show very little impact. So the chain's holiday spikes are really year end spikes.
    Top 10 vs Bottom 10 Stores:
        Further along in the exploration I ranked the 45 stores by average weekly sales. The gap I found is huge. The top performing store averages over $2 million per week, while the bottom averages $250 thousand. That's an 8 to 1 ratio. This was the most striking thing in the chain-wide data and is what led me to pivot from chain-wide analysis to investigating individual stores. At this point I could tell whatever was driving overall sales clearly wasn't distributed evenly across the 45 stores.


Regression Results:
    Economic Factors:
        The first linear regression model tested whether economic conditions could predict weekly sales. The features were Temperature, Fuel Price, Consumer Price Index, and Unemployment. The model produced an r2 of 0.0101, meaning it explained about 1% of the variation in sales. The RMSE was over $555 thousand, which is huge considering the average weekly sales per store is around $1 million. Every coefficient was negative, but none of them pointed towards any meaningful direction. This was the first formal confirmation that economic conditions alone cannot predict store sales, as well as confirmation that chain-wide analysis was not going to provide any meaningful insight.
    Time-Based Features:
        The second model was ran using time-based features. Year, Month and Week. This one performed even worse with an r2 of 0.0028. Less than half a percent of sales variation explained. The RMSE was very close to Model A. Together, these two models heavily reinforced what I found in my exploratory analysis. Chain-wide features, whether economic or time-based, cannot predict individual store sales. Moving forward the analysis will move to store-level analysis.


Pivot to store level:
    At this point it was clear to me that Chain-wide economic and time-based features didn't predict sales. But the 8 to 1 gap between the top and bottom stores from earlier in the analysis showed some promise. That gap had to be driven by something specific to the stores themselves, so the project pivoted from looking at the chain as a whole to comparing the top 10 and bottom 10 stores directly. 


Store type and size finding:
    The stores.csv dataset labled each store as Type A, B or C, but it didn't define what those types meant. To figure it out, I grouped the stores by type and looked at their square footage. Type A stores averaged around 177,000 square feet, Type B averaged around 101,000, and Type C clustered tightly around 40,000. So type is essentially a label for store scale. With that established, I cross-referenced the types with the top and bottom 10 stores. Almost every top performing store was Type A, and almost every bottom performing store was Type B or C. Size alone explained a huge portion of the gap between the best and worst performing stores.


Sales per square foot:
    I confirmed that store size was the dominant driver of raw sales. But I needed a way to compare stores fairly regardless of how big they were. Total sales would always favor the largest stores, so it doesn't give smaller stores a chance to show if they are performing well or not. So I added a new metric: sales per square foot. I calculated it by dividing each store's average weekly sales by its size, and saved it back into stores.csv as a new column. When I ranked the stores by this new metric, the story flipped. Looking at the top and bottom 3 performers within each type, Type B and C stores actually led the chain in efficiency, with the top performers reaching around $15 per square foot, while the largest Type A stores topped out around $10 per square foot. So Type A stores generate more total sales because of their size, but they aren't the most efficient. This is valuable because it changes how you might think about store performance. A small Type C store doing $500K a week looks unimpressive next to a Type A doing $2M, but if it's pulling $15 per square foot it's actually outperforming the larger store on a per-space basis. This insight is important for decisions like where to invest in expansion or where to study what's working. From here I had two complementary lenses to evaluate performance: total sales for raw output and sales per square foot for efficiency. Both matter for answering the research question.

Holiday responsiveness:
    To wrap up the store-level analysis, I looked at how holidays affected the top and bottom stores. For each store I averaged sales during holiday weeks and compared them to non-holiday weeks. The top 10 all saw a positive bump and the bottom 10 were inconsistent, but with only 10 holiday data points per store those individual percentages are unstable. The more reliable finding came when I compared holiday rankings to overall rankings. They were nearly identical. The top stores stayed on top during holidays, the bottom stores stayed at the bottom. Holidays don't reshape performance, they amplify it. The implication from this is that improving non-holiday performance should be the focus, and greater holiday performance will follow from that.

Answer to the research question:
    So back to the original question: what separates Walmart's best stores from its worst, and can we predict it? The first half has a clear answer. The biggest factor is size. Top performers are large Type A stores averaging 177,000 square feet, while bottom performers are mostly Type B and C stores under 100,000 square feet. But "best" depends on how you measure it. By raw sales, the largest stores win. By sales per square foot, the smaller stores are actually more efficient. So both lenses tell a different story about who's performing well. The second half of the question is harder. Can we predict it from the available data? The honest answer is no. The variables that do separate the stores are static structural ones like size and type that don't change week to week. The variables we have that should drive performance week to week -- temperature, fuel price, CPI, and unemployment -- failed to predict sales in regression with R-squared values under 0.01. So while I can describe what makes a store top or bottom tier, I can't reliably predict it without better data.

Confounding factors:
    The data turned out to have several confounding factors -- variables that look independent but actually are redundant information. CPI and Unemployment are the first example. They barely change within a single store over the entire 2.5 year timespan, but vary dramatically between stores. They function more as a regional identifier than an economic one. Type and Size are redundant as well, with a store's type you can reliably predict its size and vice versa. Fuel Price and Year also carry the same information since Fuel Price climbed steadily over time. These overlaps help explain why the linear regression models performed so poorly.

Data collection reccomendations:
    Based on the limitations and confounding factors I encountered within the data, I have changes to recommend to make this dataset more useful for predicting performance. First, replace CPI and Unemployment with real store location data like city, state, or region. Those variables are already acting as regional identifiers, so collecting the location directly would turn them into useful information and allow supplemental research into the locations. Second, drop or replace the redundant features. Type and Size are the same information, I would recommend dropping type and keeping the more specific size, or renaming the Type into something more descriptive of the location like "Supercenter, Discount Store, or Neighborhood Market" to give more context. Fuel Price and Year are also redundant, I would drop Fuel Price altogether or find another metric to track transportation accessibility such as public transport availability or parking capacity. Or even just track local gas prices for each individual store. Once redundancy is gone I would recommend collecting variables that drive store-level performance differences. Operational data such as staffing levels, marketing budget, product mix, and department sales would likely explain a lot of variation. Department level sales in particular would let you see what's actually selling at each store and allow direct comparison of stores of similar size. Customer data like foot traffic, demographics, and local competition would also provide great insight. Finally the time frame is just too short, two and a half years isn't enough to see real long-term trends, especially when one of those years is partial.

Thank you:
    That wraps up the analysis, thank you for taking the time to follow along. If you have any questions, feel free to reach out to me at the email on the screen. The full code, any visualizations I didn't include, and the script for this presentation are available in the GitHub repository linked here. I appreciate the opportunity to share this work.

-END-