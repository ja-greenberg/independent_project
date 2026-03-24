import pandas as pd

# Load Data
raw = pd.read_csv("amazon/data/amazon.csv")

# Standardize column names
raw.columns = raw.columns.str.strip()

# Raw data is not possible to view with head, info, or describe due to extremely long entires in many columns.
# View data structure and quality
# print("Columns:", raw.columns.tolist())
# print("Shape:", raw.shape)
# print("Dtypes:", raw.dtypes)
# print("Null values:", raw.isnull().sum())
# print("Duplicate rows:", raw.duplicated().sum())
# print("Unique counts:", raw.nunique())

# Quality checks found nulls in rating_count.
# print(raw.loc[raw["rating_count"].isnull(), ["product_id", "product_name", "rating_count"]])

# Convert rating_count to numeric for validation checks.
raw["rating_count"] = pd.to_numeric(raw["rating_count"].astype(str).str.replace(",", "", regex=False), errors="coerce")

# Check for products with a rating_count of 0.
# print(raw[raw["rating_count"] == 0][["product_id", "product_name", "rating_count"]])

# No products were found with rating_count equal to 0.
# The null values in rating_count are being kept for now because they are so few
# and may not affect the analysis unless rating_count data becomes important.

# Cleaning actions
clean = raw.copy()
# Convert appropriate columns to numeric, coercing errors to NaN.
clean["discounted_price"] = pd.to_numeric(clean["discounted_price"].astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False), errors="coerce")
clean["actual_price"] = pd.to_numeric(clean["actual_price"].astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False), errors="coerce")
# % symbol was removed from discount_percentage so the field could be stored as numeric data for analysis.
clean["discount_percentage"] = pd.to_numeric(clean["discount_percentage"].astype(str).str.replace("%", "", regex=False), errors="coerce")
clean["rating"] = pd.to_numeric(clean["rating"], errors="coerce")
clean["rating_count"] = pd.to_numeric(clean["rating_count"].astype(str).str.replace(",", "", regex=False), errors="coerce")

# Validate conversions
# print("Null values after conversion:\n", clean[["discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"]].isnull().sum())
# print("Invalid discounted_prices (<= 0):", (clean["discounted_price"] <= 0).sum())
# print("Invalid actual_prices (<= 0):", (clean["actual_price"] <= 0).sum())
# print("InvaLid discount_percentages outside 0-100:", ((clean["discount_percentage"] < 0) | (clean["discount_percentage"] > 100)).sum())
# print("Invalid ratings outside 0-5:", ((clean["rating"] < 0) | (clean["rating"] > 5)).sum())
# print("Invalid rating_counts (< 0):", (clean["rating_count"] < 0).sum())

# Data checks found null values in rating and rating_count.
# rating_count was already known to contain a small number of nulls, and it is printed here again for reference.
# print(clean.loc[clean["rating"].isnull(), ["product_id", "product_name", "rating"]])
# print(clean.loc[clean["rating_count"].isnull(), ["product_id", "product_name", "rating_count"]])

# Rows with null values in rating are dropped because rating is likely to be a core metric for analysis, records with missing or null values cannot be used reliably.
clean = clean.dropna(subset=["rating"])

# Remove duplicates
clean = clean.drop_duplicates()

# Added a discount_amount column for discount amount
clean["discount_amount"] = clean["actual_price"] - clean["discounted_price"]
# print(clean[["actual_price", "discounted_price", "discount_amount"]].head(10))

# Added a primary_category column taking the first category from each product's category list for easier analysis.
clean["primary_category"] = clean["category"].astype(str).str.split("|").str[0]
# print(clean[["category", "primary_category"]].head(10))

# Final validation checks
print("Final shape:", clean.shape)
print("Null values after cleaning:\n", clean.isnull().sum(), "\n")
print("Rating range:", clean["rating"].min(), "to", clean["rating"].max())
print("Discount percentage range:", clean["discount_percentage"].min(), "to", clean["discount_percentage"].max())
print("Discounted price range:", clean["discounted_price"].min(), "to", clean["discounted_price"].max())
print("Actual price range:", clean["actual_price"].min(), "to", clean["actual_price"].max())

# Sort by primary_category and product_name and reset index
clean = clean.sort_values(["primary_category", "product_name"]).reset_index(drop=True)

# Export cleaned dataset
clean.to_csv("amazon/data/amazon_clean.csv", index=False)