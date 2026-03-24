import pandas as pd

# Load data
raw = pd.read_csv("walmart/data/Walmart.csv")

# Standardize column names
raw.columns = raw.columns.str.strip()

# View raw data
# print(raw.head(), "\n")
# print(raw.info(), "\n")
# print(raw.describe(include="all"))

# Convert Date to datetime
raw["Date"] = pd.to_datetime(raw["Date"], dayfirst=True, errors="coerce")

# Convert Weekly_Sales to numeric in case of bad values
raw["Weekly_Sales"] = pd.to_numeric(raw["Weekly_Sales"], errors="coerce")

# Checks for nulls, duplicates, and invalid data
# print("Null values before cleaning:\n", raw.isnull().sum(), "\n")
# print("Duplicate rows before cleaning:", raw.duplicated().sum(), "\n")

# invalid_dates = raw[raw["Date"].isna()]
# print("Invalid/missing dates:", len(invalid_dates), "\n")

# invalid_sales = raw[raw["Weekly_Sales"] <= 0]
# print("Invalid sales rows (<= 0):", len(invalid_sales))

# Cleaning actions
clean = raw.copy()

# Remove rows nulls, duplicates, and negative invalid sales
clean = clean.dropna(subset=["Date"])
clean = clean.drop_duplicates()
clean = clean[clean["Weekly_Sales"] > 0]

# Feature engineering
clean["Year"] = clean["Date"].dt.year
clean["Month"] = clean["Date"].dt.month
clean["Week"] = clean["Date"].dt.isocalendar().week.astype("int64")

# Sort by date and reset index
clean = clean.sort_values("Date").reset_index(drop=True)

# Final validation checks
print("\nNull values after cleaning:\n", clean.isnull().sum(), "\n")
print("Final row count:", len(clean))
print("Date range:", clean["Date"].min(), "to", clean["Date"].max())
print("Unique dates:", clean["Date"].nunique())

# Export cleaned dataset
clean.to_csv("walmart/data/walmart_clean.csv", index=False)