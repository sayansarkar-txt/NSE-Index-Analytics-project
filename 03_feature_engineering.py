import pandas as pd

df = pd.read_csv(r"E:\NSE Index Analytics project\data\processed\nse_index_clean.csv")

# Risk score mapping
risk_map = {
    'Low': 1,
    'Medium': 2,
    'High': 3,
    'Very High': 4,
    'Extreme': 5
}

df['risk_score'] = df['risk_level'].map(risk_map)

# Return category based on 5Y CAGR
def return_category(cagr):
    if cagr >= 25:
        return 'Excellent'
    elif cagr >= 20:
        return 'Very High'
    elif cagr >= 15:
        return 'High'
    elif cagr >= 10:
        return 'Moderate'
    else:
        return 'Low'

df['return_category'] = df['cagr_5y'].apply(return_category)

# Risk-adjusted return
df['risk_adjusted_return'] = df['cagr_5y'] / df['volatility']

# Valuation score
df['valuation_score'] = df['avg_pe'] * df['avg_pb']

# Save final dataset
df.to_csv(r"E:\NSE Index Analytics project\data\processed\nse_index_final.csv", index=False)

print("✅ Feature engineering completed")