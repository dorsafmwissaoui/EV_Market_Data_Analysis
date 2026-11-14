


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


df = pd.read_csv("../data_processed/ev_market_clean.csv")

# 2. Feature Engineering: Segment vehicles by Electric Range (Miles)
def categorize_range(miles):
    if miles == 0:
        return 'Unrated (New Models)'
    elif miles < 100:
        return 'Short Range (< 100 mi)'
    elif miles <= 200:
        return 'Medium Range (100 - 200 mi)'
    else:
        return 'Long Range (> 200 mi)'

df['Range_Category'] = df['Electric Range'].apply(categorize_range)

print("=== Vehicle Segmentation by Electric Range ===")
print(df['Range_Category'].value_counts())

# 3. Top 10 EV Manufacturers (Market Share)
top_makes = df['Make'].value_counts().head(10)
print(f"\nTesla Market Share: {(top_makes['TESLA'] / len(df)) * 100:.2f}%")

plt.figure(figsize=(10, 6))
sns.barplot(x=top_makes.values, y=top_makes.index, palette="viridis")
plt.title("Top 10 Electric Vehicle Manufacturers in Washington State", fontsize=14, fontweight='bold')
plt.xlabel("Number of Registered Vehicles", fontsize=12)
plt.ylabel("Manufacturer (Make)", fontsize=12)
plt.tight_layout()
plt.savefig("top_10_ev_makes.png", dpi=300)
plt.close()

# 4. Geographic Concentration: Top 10 Cities in Washington
top_cities = df['City'].value_counts().head(10)
print("\n=== Top 10 Cities for EV Adoption ===")
print(top_cities)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_cities.values, y=top_cities.index, palette="magma")
plt.title("Top 10 Cities by Electric Vehicle Concentration", fontsize=14, fontweight='bold')
plt.xlabel("Number of Registered Vehicles", fontsize=12)
plt.ylabel("City", fontsize=12)
plt.tight_layout()
plt.savefig("top_10_ev_cities.png", dpi=300)
plt.close()

# 5. EV Growth Trend (2011 - 2023)
yearly_growth = df[(df['Model Year'] >= 2011) & (df['Model Year'] <= 2023)]['Model Year'].value_counts().sort_index()

plt.figure(figsize=(10, 5))
sns.lineplot(x=yearly_growth.index, y=yearly_growth.values, marker="o", linewidth=2.5, color="#1f77b4")
plt.title("Electric Vehicle Adoption Growth Trend (2011 - 2023)", fontsize=14, fontweight='bold')
plt.xlabel("Model Year", fontsize=12)
plt.ylabel("Number of Vehicles", fontsize=12)
plt.xticks(yearly_growth.index)
plt.tight_layout()
plt.savefig("ev_growth_trend.png", dpi=300)
plt.close()

# 6. BEV vs PHEV Market Split
ev_types = df['Electric Vehicle Type'].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(ev_types.values, labels=ev_types.index, autopct='%1.1f%%', startangle=140, colors=["#1f77b4", "#d62728"], wedgeprops={'width': 0.4})
plt.title("Market Share: Full Electric (BEV) vs. Plug-in Hybrid (PHEV)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("bev_vs_phev_share.png", dpi=300)
plt.close()

# 7. Tax & Policy Impact (CAFV Eligibility)
cafv_stats = df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts(normalize=True) * 100
print("\n=== Tax Incentive Eligibility (CAFV %) ===")
print(cafv_stats.round(2))

print("\nAll 4 high-resolution charts generated successfully!")
