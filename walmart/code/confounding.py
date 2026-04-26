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

# Confounding Factor 1: CPI and Unemployment are store identity proxies

# Show how much CPI and Unemployment vary WITHIN each store vs BETWEEN stores
store_variation = df.groupby("Store").agg(
    CPI_mean=("CPI", "mean"),
    CPI_std=("CPI", "std"),
    Unemp_mean=("Unemployment", "mean"),
    Unemp_std=("Unemployment", "std")
)

print("CPI and Unemployment variation within each store:")
print(store_variation.to_string())

print(f"\n--- Summary ---")
print(f"Average Consumer Price Index (CPI) std within a store: {store_variation['CPI_std'].mean():.2f}")
print(f"Consumer Price Index (CPI) std across store means:     {store_variation['CPI_mean'].std():.2f}")
print(f"Average Unemployment std within a store:               {store_variation['Unemp_std'].mean():.2f}")
print(f"Unemployment std across store means:                   {store_variation['Unemp_mean'].std():.2f}")

# Visualization: CPI clusters by store

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# CPI per store
axes[0].scatter(store_variation.index, store_variation["CPI_mean"], color=palette[0], s=60, alpha=0.8)
axes[0].set_title("Average CPI by Store", fontsize=14)
axes[0].set_xlabel("Store", fontsize=12)
axes[0].set_ylabel("Average CPI", fontsize=12)

# Unemployment per store
axes[1].scatter(store_variation.index, store_variation["Unemp_mean"], color=palette[3], s=60, alpha=0.8)
axes[1].set_title("Average Unemployment by Store", fontsize=14)
axes[1].set_xlabel("Store", fontsize=12)
axes[1].set_ylabel("Average Unemployment (%)", fontsize=12)

plt.suptitle("CPI and Unemployment Cluster by Store -- Evidence of Regional Confounding", fontsize=15)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
print("\n")
# Confounding Factor 2: Type and Size are redundant

# How much Size varies within each Type
type_size = stores.groupby("Type")["Size"].agg(["mean", "std", "min", "max", "count"])
print("Size statistics by Type:")
print(type_size)

# Correlation between Type and Size
type_numeric = {"A": 0, "B": 1, "C": 2}
stores["Type_Numeric"] = stores["Type"].map(type_numeric)
print(f"\nCorrelation between Type and Size: {stores['Type_Numeric'].corr(stores['Size']):.3f}")
print("\n")

# ********** Confounding Factor 3: Fuel Price and Year are redundant **********

# Average fuel price by year
fuel_by_year = df.groupby("Year")["Fuel_Price"].agg(["mean", "min", "max"])
print("Fuel Price by Year:")
print(fuel_by_year)

# Correlation
print(f"\nCorrelation between Fuel_Price and Year: {df['Fuel_Price'].corr(df['Year']):.3f}")
print("\n")