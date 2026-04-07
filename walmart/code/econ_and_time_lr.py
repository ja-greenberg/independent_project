import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("walmart/data/walmart_clean.csv")

# Model A: Predict weekly sales based on economic factors. (Temperature, fuel price, CPI, unemployment rate)

# Select the features and variable
economic_features = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
X_economic = df[economic_features]
y = df['Weekly_Sales']

# Split intro training and testing
X_train, X_test, y_train, y_test = train_test_split(X_economic, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train
model_economic = LinearRegression()
model_economic.fit(X_train_scaled, y_train)

# Predict
y_pred_economic = model_economic.predict(X_test_scaled)

# Evaluate
print("Model A: Economic Factors")
print(f"r2: {r2_score(y_test, y_pred_economic):.4f}")
print(f"rmse: {np.sqrt(mean_squared_error(y_test, y_pred_economic)):.4f}")
print(f"mae: {mean_absolute_error(y_test, y_pred_economic):.4f}")
# Coefficients
print("\n  Coefficients (standardized):")
for name, coef in sorted(zip(economic_features, model_economic.coef_),
                          key=lambda x: abs(x[1]), reverse=True):
    direction = "+" if coef > 0 else "-"
    print(f"    {name:<16} {coef:>12,.0f}  ({direction} sales)")


# Model B: Predict weekly sales on time based features. (Week, Month, Year)

# Select the features and variable
time_features = ['Week', 'Month', 'Year']
X_time = df[time_features]

# Split intro training and testing
X_train, X_test, y_train, y_test = train_test_split(X_time, y, test_size=0.2, random_state=42)

# Train
model_time = LinearRegression()
model_time.fit(X_train, y_train)

# Predict
y_pred_time = model_time.predict(X_test)

# Evaluate
print("\nModel B: Time-Based Features")
print(f"r2: {r2_score(y_test, y_pred_time):.4f}")
print(f"rmse: {np.sqrt(mean_squared_error(y_test, y_pred_time)):.4f}")
print(f"mae: {mean_absolute_error(y_test, y_pred_time):.4f}")

# Coefficients
print("\n  Coefficients:")
for name, coef in sorted(zip(time_features, model_time.coef_),
                          key=lambda x: abs(x[1]), reverse=True):
    direction = "+" if coef > 0 else "-"
    print(f"    {name:<16} {coef:>12,.0f}  ({direction} sales)")

