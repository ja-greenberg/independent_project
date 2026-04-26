import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

sns.set_style("whitegrid")
palette = sns.color_palette("muted")

df = pd.read_csv("walmart/data/walmart_clean.csv")
stores = pd.read_csv("walmart/data/stores.csv")
df = df.merge(stores, on="Store")
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# Rank stores by average weekly sales
store_avg_sales = df.groupby("Store")["Weekly_Sales"].mean().sort_values(ascending=False)
top10 = store_avg_sales.head(10).index.to_list()
bot10 = store_avg_sales.tail(10).index.to_list()

top10_info = df[df["Store"].isin(top10)].groupby("Store").agg(
    Type=("Type", "first"),
    Size=("Size", "first"),
    Avg_Weekly_Sales=("Weekly_Sales", "mean")
).sort_values("Avg_Weekly_Sales", ascending=False)

bot10_info = df[df["Store"].isin(bot10)].groupby("Store").agg(
    Type=("Type", "first"),
    Size=("Size", "first"),
    Avg_Weekly_Sales=("Weekly_Sales", "mean")
).sort_values("Avg_Weekly_Sales", ascending=False)

print("Top 10 Stores by Average Weekly Sales:")
print(top10_info)
print("\nBottom 10 Stores by Average Weekly Sales:")
print(bot10_info)

# Sales per square foot by store
store_performance = df.groupby("Store").agg(
    Avg_Weekly_Sales=("Weekly_Sales", "mean"),
    Size=("Size", "first"),
    Type=("Type", "first")
)

store_performance["Sales_per_SqFt"] = store_performance["Avg_Weekly_Sales"] / store_performance["Size"]

# Save enriched stores data
store_performance[["Type", "Size", "Avg_Weekly_Sales", "Sales_per_SqFt"]].reset_index().to_csv("walmart/data/stores.csv", index=False)

# Top and bottom 3 performers within each type
for store_type in ["A", "B", "C"]:
    type_stores = store_performance[store_performance["Type"] == store_type].sort_values("Sales_per_SqFt", ascending=False)
    print(f"\n--- Type {store_type} Stores (by Sales per Sq Ft) ---")
    print(f"Top 3:")
    print(type_stores.head(3)[["Size", "Avg_Weekly_Sales", "Sales_per_SqFt"]])
    print(f"Bottom 3:")
    print(type_stores.tail(3)[["Size", "Avg_Weekly_Sales", "Sales_per_SqFt"]])

# Visualization: Sales per square foot by store type
fig, ax = plt.subplots(figsize=(10, 6))

type_colors = {"A": palette[0], "B": palette[2], "C": palette[3]}

for store_type, color in type_colors.items():
    group = store_performance[store_performance["Type"] == store_type]
    ax.scatter(group["Size"], group["Sales_per_SqFt"], color=color, s=80, alpha=0.7,
               label=f"Type {store_type}", edgecolors="white", linewidth=0.5)

ax.set_title("Sales per Square Foot vs Store Size (by Type)", fontsize=16)
ax.set_xlabel("Store Size (sq ft)", fontsize=12)
ax.set_ylabel("Sales per Sq Ft ($)", fontsize=12)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x/1e3:.0f}K"))
ax.legend(title="Store Type")
plt.tight_layout()
plt.show()

# When normalized by size the performance story changes. Type A stores originally had the highest average weekly sales, but now we see that Type B and C stores have higher sales per square foot. 
# This suggests that while Type A stores are larger and generate more total sales, they may not be utilizing their space as efficiently as the smaller Type B and C stores. 
# Type B also had the widest variation in sales, suggesting this type of store would benefit the most from targeted improvements.
# This leaves us with two different metrics to evaluate store performance: total sales and sales per square foot.

# Add sales per sqft to stores data
stores = store_performance[["Type", "Size", "Avg_Weekly_Sales", "Sales_per_SqFt"]].reset_index()
stores.to_csv("walmart/data/stores.csv", index=False)
# print(stores.sort_values(["Type", "Sales_per_SqFt"], ascending=[True, False]).to_string(index=False))

# Holiday effect on top and bottom performers

# Holiday and non-holiday sales for top 10 stores
top10_sales = df[df["Store"].isin(top10)].groupby(["Store", "Holiday_Flag"])["Weekly_Sales"].mean().unstack()
top10_nonholiday = top10_sales[0]
top10_holiday = top10_sales[1]

# Holiday and non-holiday sales for bottom 10 stores
bot10_sales = df[df["Store"].isin(bot10)].groupby(["Store", "Holiday_Flag"])["Weekly_Sales"].mean().unstack()
bot10_nonholiday = bot10_sales[0]
bot10_holiday = bot10_sales[1]

# Dollar and percentage difference between holiday and non-holiday
top10_diff = top10_holiday - top10_nonholiday
top10_pct_diff = (top10_diff / top10_nonholiday) * 100

bot10_diff = bot10_holiday - bot10_nonholiday
bot10_pct_diff = (bot10_diff / bot10_nonholiday) * 100

print("\nHoliday vs Non-Holiday Sales for Top 10 Stores:")
print(pd.DataFrame({
    "Non-Holiday Sales": top10_nonholiday,
    "Holiday Sales": top10_holiday,
    "Difference ($)": top10_diff,
    "Difference (%)": top10_pct_diff
}).sort_values("Holiday Sales", ascending=False).to_string(float_format="{:,.2f}".format))

print("\nHoliday vs Non-Holiday Sales for Bottom 10 Stores:")
print(pd.DataFrame({
    "Non-Holiday Sales": bot10_nonholiday,
    "Holiday Sales": bot10_holiday,
    "Difference ($)": bot10_diff,
    "Difference (%)": bot10_pct_diff
}).sort_values("Holiday Sales", ascending=False).to_string(float_format="{:,.2f}".format))

# Holiday responsiveness varies widely across stores. Top 10 see a positive holiday bump, but the bottom 10 are inconsistent. However, with only 10 holiday datapoints per store it is hard to draw strong conclusions.
# More importantly, holiday sales rankings nearly perfectly mirror overall sales rankings for both groups, meaning holidays are amplifying existing performance rather than reshuffling.
# This suggests holiday performance is a reflection of overall performance. Improving non-holiday sales should be the primary focus, and holiday sales will improve in turn.