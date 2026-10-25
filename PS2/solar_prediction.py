import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load the dataset
df = pd.read_csv("SolarPrediction.csv")

# 2. Select weather features and target
features = [
    "Temperature",
    "Pressure",
    "Humidity",
    "WindDirection(Degrees)",
    "Speed"
]

X = df[features]
y = df["Radiation"]

# 3. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train the model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# 5. Predict radiation on the test set
predictions = model.predict(X_test)

# 6. Evaluate the model
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("SOLAR RADIATION PREDICTION RESULTS")
print("----------------------------------")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"R² Score: {r2:.3f}")

# 7. Plot actual vs predicted radiation
plt.figure(figsize=(8, 6))
plt.scatter(y_test, predictions, alpha=0.35, s=12)

# Reference line for perfect predictions
maximum = max(y_test.max(), predictions.max())
plt.plot([0, maximum], [0, maximum], "r--")

plt.xlabel("Actual Solar Radiation")
plt.ylabel("Predicted Solar Radiation")
plt.title("Actual vs Predicted Solar Radiation")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("actual_vs_predicted_radiation.png", dpi=300)
plt.show()