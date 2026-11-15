


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, accuracy_score, mean_absolute_error

sns.set_theme(style="whitegrid")

# 1. Load cleaned dataset
df = pd.read_csv("../data_processed/ev_market_clean.csv")

print("==========================================================")
print("   MODEL 1: PREDICTING ELECTRIC RANGE (REGRESSION)        ")
print("==========================================================")

# Filter vehicles with tested electric range (> 0) for training
tested_df = df[df['Electric Range'] > 0].copy()

# Encode categorical columns (Make, Model, Electric Vehicle Type) into numbers
le_make = LabelEncoder()
le_model = LabelEncoder()
le_type = LabelEncoder()

tested_df['Make_Encoded'] = le_make.fit_transform(tested_df['Make'])
tested_df['Model_Encoded'] = le_model.fit_transform(tested_df['Model'])
tested_df['Type_Encoded'] = le_type.fit_transform(tested_df['Electric Vehicle Type'])

X_reg = tested_df[['Model Year', 'Make_Encoded', 'Model_Encoded', 'Type_Encoded']]
y_reg = tested_df['Electric Range']

# Split data: 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# Train Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Evaluate model accuracy
y_pred_reg = rf_model.predict(X_test)
r2 = r2_score(y_test, y_pred_reg)
mae = mean_absolute_error(y_test, y_pred_reg)

print(f"R2 Accuracy Score: {r2 * 100:.2f}%")
print(f"Mean Absolute Error (MAE): {mae:.2f} miles")


print("\n==========================================================")
print("   MODEL 2: TAX INCENTIVE ELIGIBILITY (CLASSIFICATION)    ")
print("==========================================================")

# Keep known eligibility records (Eligible vs Not Eligible)
clf_df = tested_df[tested_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].isin(['Eligible', 'Not Eligible (Low Range)'])].copy()

X_clf = clf_df[['Model Year', 'Make_Encoded', 'Type_Encoded', 'Electric Range']]
y_clf = clf_df['Clean Alternative Fuel Vehicle (CAFV) Eligibility']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

# Train Decision Tree Classifier
dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train_c, y_train_c)

y_pred_clf = dt_model.predict(X_test_c)
acc = accuracy_score(y_test_c, y_pred_clf)
print(f"Classification Accuracy: {acc * 100:.2f}%")





print("\n==========================================================")
print("   MODEL 3: FUTURE EV MARKET FORECASTING (2024 - 2028)    ")
print("==========================================================")

# Prepare historical yearly registrations (2013 - 2023)
yearly_data = df[(df['Model Year'] >= 2013) & (df['Model Year'] <= 2023)].groupby('Model Year').size().reset_index(name='Registrations')

X_time = yearly_data[['Model Year']]
y_time = yearly_data['Registrations']

# Use Polynomial Regression (degree=2) to capture exponential EV growth curve
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_time)

trend_model = LinearRegression()
trend_model.fit(X_poly, y_time)

# Predict through future years: 2024 to 2028
target_years = list(range(2024, 2029))
future_years = pd.DataFrame({'Model Year': target_years})
future_poly = poly.transform(future_years)
future_preds = trend_model.predict(future_poly).round(0).astype(int)

forecast_df = pd.DataFrame({'Model Year': target_years, 'Predicted Registrations': future_preds})
print("Forecasted EV Registrations (2024 - 2028):")
print(forecast_df.to_string(index=False))

# Plot Historical Data + Future Predictions up to 2028
plt.figure(figsize=(11, 5))
plt.plot(yearly_data['Model Year'], yearly_data['Registrations'], marker='o', linewidth=2.5, label='Historical Data (2013-2023)', color='#1f77b4')
plt.plot(forecast_df['Model Year'], forecast_df['Predicted Registrations'], marker='s', linestyle='--', linewidth=2.5, label='ML Forecast (2024-2028)', color='#d62728')

for x, y in zip(forecast_df['Model Year'], forecast_df['Predicted Registrations']):
    plt.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, fontweight='bold', color='#d62728')

plt.title("EV Market Growth & Future ML Forecast (2013 - 2028)", fontsize=14, fontweight='bold')
plt.xlabel("Model Year", fontsize=12)
plt.ylabel("Number of Registered Vehicles", fontsize=12)
plt.xticks(list(range(2013, 2029)))
plt.legend()
plt.tight_layout()
plt.savefig("ev_future_forecast.png", dpi=300)
plt.close()


print("\n==========================================================")
print("   MODEL 4: TOP 5 BRANDS DEMAND FORECAST (2027 & 2028)    ")
print("==========================================================")

top_5_brands = df['Make'].value_counts().head(5).index
brand_forecasts = []

for brand in top_5_brands:
    brand_yearly = df[(df['Make'] == brand) & (df['Model Year'] >= 2015) & (df['Model Year'] <= 2023)].groupby('Model Year').size().reset_index(name='Count')
    if len(brand_yearly) > 2:
        X_b = brand_yearly[['Model Year']]
        y_b = brand_yearly['Count']
        b_model = LinearRegression()
        b_model.fit(X_b, y_b)
       
        future_b = pd.DataFrame({'Model Year': list(range(2027, 2029))})
        preds_b = b_model.predict(future_b).round(0).astype(int)
       
        brand_forecasts.append({
            'Brand': brand,
            'Forecast_2027': max(0, preds_b.item(0)),
            'Forecast_2028': max(0, preds_b.item(1))
        })

brand_forecast_df = pd.DataFrame(brand_forecasts).sort_values(by='Forecast_2028', ascending=False)
print(brand_forecast_df.to_string(index=False))


print("\nForecast chart saved successfully as 'ev_future_forecast.png'!")

