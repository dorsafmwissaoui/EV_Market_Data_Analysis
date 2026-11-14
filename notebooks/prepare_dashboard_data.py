import pandas as pd

df = pd.read_csv("../data_processed/ev_market_clean.csv")

# Filter years 2011 to 2023 for clean trend analysis and keep top 10 brands
top_10_makes = df['Make'].value_counts().head(10).index
df_filtered = df[(df['Model Year'] >= 2011) & (df['Model Year'] <= 2023) & (df['Make'].isin(top_10_makes))]

# Aggregate data into a lightweight summary table for Google Sheets Dashboard
dashboard_summary = df_filtered.groupby(['Model Year', 'Make', 'Electric Vehicle Type']).agg(
    Vehicle_Count=('Model', 'count'),
    Avg_Electric_Range=('Electric Range', 'mean')
).reset_index()

dashboard_summary['Avg_Electric_Range'] = dashboard_summary['Avg_Electric_Range'].round(1)

output_path = "../data_processed/ev_dashboard_summary.csv"
dashboard_summary.to_csv(output_path, index=False)

print(f"Dashboard summary created successfully! Rows: {len(dashboard_summary)}")
print(dashboard_summary.head(10))
