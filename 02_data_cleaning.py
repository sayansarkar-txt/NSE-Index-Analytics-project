import pandas as pd

# Load raw data
df = pd.read_csv(r"E:\NSE Index Analytics project\data\raw\nse_index_raw.csv")

# Standardize column names
df.columns = df.columns.str.lower().str.strip()

# Numeric columns
num_cols = [
    'cagr_1y',
    'cagr_3y',
    'cagr_5y',
    'volatility',
    'avg_pe',
    'avg_pb',
    'index_level'
]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove rows with missing values
df = df.dropna()

# Save clean data
df.to_csv(r"E:\NSE Index Analytics project\data\processed\nse_index_clean.csv", index=False)

print("✅ Data cleaned successfully")