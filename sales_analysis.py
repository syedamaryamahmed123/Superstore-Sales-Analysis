# ============================================
# Superstore Sales Analysis Project
# Tools: SQL, Python, Pandas, NumPy, Seaborn
# ============================================

# ---------- 1. Import Libraries ----------
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sqlalchemy import create_engine

plt.style.use("seaborn-v0_8")

# ---------- 2. Connect to MySQL ----------
engine = create_engine(
    "mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/super_store_dataset"
)

query = "SELECT * FROM `sample - superstore`"
df = pd.read_sql(query, engine)

# ---------- 3. Data Cleaning ----------
# Standardize column names
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(' ', '_')
      .str.replace('-', '_')
)

# Convert date columns
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

# Convert numeric columns
numeric_cols = ['sales', 'quantity', 'discount', 'profit']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove duplicates
df = df.drop_duplicates()

# ---------- 4. Feature Engineering ----------
df['profit_margin'] = df['profit'] / df['sales']

# Running sales by region
df = df.sort_values(['region', 'order_date'])
df['running_sales'] = df.groupby('region')['sales'].cumsum()

# ---------- 5. Descriptive Statistics ----------
total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
overall_profit_margin = (total_profit / total_sales) * 100

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Overall Profit Margin:", round(overall_profit_margin, 2), "%")

print("\nBasic Statistical Summary:")
print(df.describe())

# ---------- 6. Normality Test ----------
print("\nShapiro-Wilk Normality Test (Sampled Data)")

for col in ['sales', 'profit']:
    sample_data = df[col].dropna().sample(500, random_state=42)
    stat, p = stats.shapiro(sample_data)
    print(f"{col} → p-value: {round(p,4)}")

    if p > 0.05:
        print("   Likely Normally Distributed")
    else:
        print("   Not Normally Distributed")

# ---------- 7. Aggregations ----------
sales_by_region = df.groupby('region')['sales'].sum().sort_values(ascending=False)
profit_by_category = df.groupby('category')['profit'].sum().sort_values(ascending=False)

top_10_customers = (
    df.groupby('customer_name')['sales']
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

loss_customers = (
    df.groupby('customer_name')['profit']
      .sum()
      .sort_values()
      .head(10)
)

# ---------- 8. Correlation Analysis ----------
correlation_matrix = df[['sales','quantity','discount','profit']].corr()

# ---------- 9. Visualization ----------

# Sales Distribution
plt.figure(figsize=(8,6))
sns.histplot(df['sales'], bins=50)
plt.title('Distribution of Sales')
plt.xlabel('Sales Amount')
plt.ylabel('Frequency')
plt.show()

# Profit vs Sales Scatter
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='sales', y='profit')
plt.title('Profit vs Sales')
plt.show()

# Correlation Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Boxplot by Category
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x='category', y='sales')
plt.title('Sales Distribution by Category')
plt.show()

# ---------- 10. Export Clean Dataset ----------
df.to_csv("clean_sales_data.csv", index=False)

print("\nAnalysis Completed Successfully.")