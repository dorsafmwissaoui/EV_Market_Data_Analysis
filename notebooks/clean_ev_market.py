import pandas as pd


raw_path = "../data_raw/Electric_Vehicle_Population_Data.csv"
df = pd.read_csv(raw_path)

print(f"Initial dataset shape: {df.shape}")

#  Drop columns not needed for business & market analysis
cols_to_drop = ['VIN (1-10)', 'DOL Vehicle ID', '2020 Census Tract', 'Legislative District', 'Vehicle Location']
df_clean = df.drop(columns=cols_to_drop)

#  Drop rows with missing values in critical columns (less than 0.2% of total data)
df_clean = df_clean.dropna(subset=['County', 'City', 'Postal Code', 'Model', 'Electric Range', 'Base MSRP', 'Electric Utility'])

#  Simplify Electric Vehicle Type labels for cleaner visualizations
ev_type_mapping = {
    'Battery Electric Vehicle (BEV)': 'BEV (Full Electric)',
    'Plug-in Hybrid Electric Vehicle (PHEV)': 'PHEV (Plug-in Hybrid)'
}
df_clean['Electric Vehicle Type'] = df_clean['Electric Vehicle Type'].replace(ev_type_mapping)

#  Simplify CAFV Eligibility text
cafv_mapping = {
    'Clean Alternative Fuel Vehicle Eligible': 'Eligible',
    'Eligibility unknown as battery range has not been researched': 'Unknown (Not Researched)',
    'Not eligible due to low battery range': 'Not Eligible (Low Range)'
}
df_clean['Clean Alternative Fuel Vehicle (CAFV) Eligibility'] = df_clean['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].replace(cafv_mapping)

#  Check descriptive stats for Electric Range and Base MSRP
print("\n=== Cleaned Numerical Summary ===")
print(df_clean[['Model Year', 'Electric Range', 'Base MSRP']].describe())

print(f"\nCleaned dataset shape: {df_clean.shape}")
print(f"Remaining missing values:\n{df_clean.isnull().sum()}")

#  Save the cleaned dataset to data_processed
output_path = "../data_processed/ev_market_clean.csv"
df_clean.to_csv(output_path, index=False)
print(f"\nSuccessfully saved cleaned dataset to: {output_path}")
