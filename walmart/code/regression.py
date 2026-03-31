import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# Model A: Predict weekly sales based on economic factors. (Temperature, fuel price, CPI, unemployment rate)

df = pd.read_csv("walmart_sales.csv")
