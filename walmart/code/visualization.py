import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np

df = pd.read_csv("walmart/data/walmart_clean.csv")
df["Date"] = pd.to_datetime(df["Date"])

sns.set_style("white")
palette = sns.color_palette("muted")

# ********** Visualization 1: Total Weekly Sales Over Time with Holiday Highlights **********
# Group by date and sum weekly sales across all stores
weekly_total_sales = df.groupby("Date")["Weekly_Sales"].sum().sort_index()

# Map each holiday date to its holiday name based on month
def get_holiday_name(date):
    month = date.month
    if month == 2:
        return "Super Bowl"
    elif month == 9:
        return "Labor Day"
    elif month == 11:
        return "Thanksgiving / Black Friday"
    elif month == 12:
        return "Christmas / New Year"
    return "Unknown"

# Each tracked holiday gets a specific color for easy identification on the plot.
holiday_colors = {
    "Super Bowl": "red",
    "Labor Day": "green",
    "Thanksgiving / Black Friday": "orange",
    "Christmas / New Year": "purple",
}

# Plot total weekly sales over time
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(weekly_total_sales.index, weekly_total_sales.values, color=palette[0], linewidth=1.2,
        label="Total Weekly Sales")

# Highlight holiday weeks with color-coded vertical lines
holiday_dates = df[df["Holiday_Flag"] == 1]["Date"].unique()
already_labeled = set()

for holiday in sorted(holiday_dates):
    name = get_holiday_name(holiday)
    ax.axvline(holiday, color=holiday_colors[name], alpha=0.5, linewidth=1.5,
               label=name if name not in already_labeled else "")
    already_labeled.add(name)

ax.set_title("Total Weekly Sales Over Time", fontsize=16)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Total Weekly Sales ($)", fontsize=12)

# Show a label every 3 months
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation=45, ha="right")

# Format y-axis as $XXM
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x/1e6:.0f}M"))

ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig("walmart/visualizations/vis1_total_weekly_sales_over_time.png", dpi=300)
plt.show()

# ********** Visualization 2: Bar chart of average sales by month **********

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Extract month from date
df["Month_Name"] = df["Date"].dt.month_name()

monthly_avg_sales = df.groupby("Month_Name")["Weekly_Sales"].mean().reindex(months)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(monthly_avg_sales.index, monthly_avg_sales.values, color=palette[0], alpha=0.7)

# Highlight three peak months with a orange
peak_months = monthly_avg_sales.sort_values(ascending=False).head(3).index
for bar, month in zip(bars, monthly_avg_sales.index):
    if month in peak_months:
        bar.set_color(palette[3])

ax.set_title("Average Weekly Sales by Month", fontsize=16)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Average Weekly Sales ($)", fontsize=12)
ax.set_ylim(800000, 1350000)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x/1e6:.2f}M"))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("walmart/visualizations/vis2_avg_sales_per_month.png", dpi=300)
plt.show()

# ********** Visualization 3: Holiday vs non holiday weeks bar chart **********
holiday_avg = df.groupby("Holiday_Flag")["Weekly_Sales"].mean()

# Count weeks in each group
holiday_counts = df.groupby("Holiday_Flag")["Weekly_Sales"].count()
labels = [f"Non-Holiday\n(n = {holiday_counts[0]:,} weeks)", f"Holiday\n(n = {holiday_counts[1]:,} weeks)"]

fig, ax = plt.subplots(figsize=(6, 5))
colors = [palette[0], palette[3]] 
bars = ax.bar(labels, holiday_avg.values, color=colors, alpha=0.7)

# Display each bars value
for bar in bars:
    height = bar.get_height()
    ax.annotate(f"${height/1e6:.2f}M",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom')

ax.set_title("Average Weekly Sales: Holiday vs Non-Holiday Weeks", fontsize=16)
ax.set_ylabel("Average Weekly Sales ($)", fontsize=12)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x/1e6:.2f}M"))
ax.set_ylim(0, max(holiday_avg.values) * 1.2)
plt.tight_layout()
plt.savefig("walmart/visualizations/vis3_holidayweeks_vs_nonholiday.png", dpi=300)
plt.show()

# ********** Visualization 4: Top 10 and Bottom 10 stores by avg sales **********

store_avg_sales = df.groupby("Store")["Weekly_Sales"].mean().sort_values(ascending=False)
top10 = store_avg_sales.head(10)
bottom10 = store_avg_sales.tail(10)

fig, ax = plt.subplots(1, 2, figsize=(12, 6), sharex=True)

# Top 10 in blue
ax[0].barh(top10.index.astype(str), top10.values, color=palette[0], alpha=0.7)
ax[0].set_title("Top 10 Stores by Average Weekly Sales", fontsize=14)
ax[0].set_xlabel("Average Weekly Sales ($)", fontsize=12)
ax[0].set_ylabel("Store", fontsize=12)
ax[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x/1e6:.2f}M"))
ax[0].invert_yaxis()

# Bottom 10 in orange
ax[1].barh(bottom10.index.astype(str), bottom10.values, color=palette[3], alpha=0.7)
ax[1].set_title("Bottom 10 Stores by Average Weekly Sales", fontsize=14)
ax[1].set_xlabel("Average Weekly Sales ($)", fontsize=12)
ax[1].set_ylabel("Store", fontsize=12)
ax[1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x/1e6:.2f}M"))
ax[1].invert_yaxis()

plt.tight_layout()
plt.savefig("walmart/visualizations/vis4_top10_bottom10_stores.png", dpi=300)
plt.show()

# ********** Visualization 5: Correlation heatmap **********

correlation_cols = ["Weekly_Sales", "Temperature", "Fuel_Price", "CPI", "Unemployment", "Holiday_Flag", "Year", "Month"]
correlation = df[correlation_cols].corr()

# Create a mask for the upper triangle? I dunno coilot kept suggesting I did this to reduce clutter. Maybe it looks nice?
mask = np.triu(np.ones_like(correlation, dtype=bool))

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)

ax.set_title("Correlation Heatmap of Key Variables", fontsize=16)
plt.tight_layout()
plt.savefig("walmart/visualizations/vis5_correlation_heatmap.png", dpi=300)
plt.show()

# ********** Visualization 6: Sales vs Economic indicators scatter plots **********

economic_vars = ["Temperature", "Fuel_Price", "CPI", "Unemployment"]
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for ax, feat, color in zip(axes.flat, economic_vars, [palette[0], palette[2], palette[3], palette[4]]):
    ax.scatter(df[feat], df["Weekly_Sales"], alpha=0.15, s=8, color=color)

    # Trend line
    trend = np.polyfit(df[feat], df["Weekly_Sales"], 1)
    line = np.linspace(df[feat].min(), df[feat].max(), 100)
    ax.plot(line, trend[0] * line + trend[1], color="black", linestyle="--", linewidth=1)

    ax.set_title(f"Weekly Sales vs {feat}", fontsize=14)
    ax.set_xlabel(feat, fontsize=12)
    ax.set_ylabel("Weekly Sales ($)", fontsize=12)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x/1e6:.2f}M"))

plt.suptitle("Weekly Sales vs Economic Indicators", fontsize=16)
plt.tight_layout()
plt.savefig("walmart/visualizations/vis6_sales_vs_economic_indicators_scatter.png", dpi=300)
plt.show()

# ********** Visualization 7: Year-over-year comparison **********

fig, ax = plt.subplots(figsize=(12, 5))

for year, color in zip(sorted(df["Year"].unique()), [palette[0], palette[2], palette[3]]):
    yearly = df[df["Year"] == year].groupby("Week")["Weekly_Sales"].mean().sort_index()
    ax.plot(yearly.index, yearly.values, label=str(year), color=color, linewidth=1.5)

# Holiday weeks and their names
holiday_labels = {
    6: "Super Bowl",
    36: "Labor Day",
    47: "Thanksgiving",
    52: "Christmas"
}

for week, name in holiday_labels.items():
    ax.axvline(week, color="gray", alpha=0.3, linewidth=1.5, linestyle="--")
    ax.annotate(name, xy=(week, ax.get_ylim()[1]), xytext=(5, -5),
                textcoords="offset points", fontsize=9, fontstyle="italic",
                ha="left", va="top")

ax.set_title("Year-over-Year: Avg Weekly Sales by Week Number", fontsize=16)
ax.set_xlabel("Week of Year", fontsize=12)
ax.set_ylabel("Avg Weekly Sales ($)", fontsize=12)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"${x/1e6:.2f}M"))
ax.legend(title="Year")
plt.tight_layout()
plt.savefig("walmart/visualizations/vis7_year_over_year_comparison_line.png", dpi=300)
plt.show()