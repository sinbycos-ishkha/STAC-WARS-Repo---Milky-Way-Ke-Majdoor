import pandas as pd

df = pd.read_csv("SolarPrediction.csv")

print("Dataset loaded successfully!")
print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset dimensions:")
print(df.shape)
print("\n--- Dataset Information ---")
print(df.info())

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Statistical Summary ---")
print(df.describe())
print("\n--- Exact Column Names ---")

for column in df.columns:
    print(repr(column))
import matplotlib.pyplot as plt

# Convert the Date column into a proper date format
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

# Convert Unix timestamps into readable dates
df["DateTime"] = pd.to_datetime(
    df["UNIXTime"], unit="s", errors="coerce"
)

# Sort observations by date and time
df = df.sort_values("DateTime")

# Plot solar radiation over time
plt.figure(figsize=(12, 5))
plt.plot(
    df["DateTime"],
    df["Radiation"],
    linewidth=0.6
)

plt.title("Solar Radiation Over Time")
plt.xlabel("Date and Time")
plt.ylabel("Solar Radiation")
plt.xticks(rotation=30)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("solar_radiation_over_time.png", dpi=300)
plt.show()
# Relationship between temperature and solar radiation
plt.figure(figsize=(8, 5))

plt.scatter(
    df["Temperature"],
    df["Radiation"],
    alpha=0.3,
    s=10
)

plt.title("Temperature vs Solar Radiation")
plt.xlabel("Temperature")
plt.ylabel("Solar Radiation")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("temperature_vs_radiation.png", dpi=300)
plt.show()

# Third graph: Humidity vs Solar Radiation
plt.figure(figsize=(8, 5))

plt.scatter(
    df["Humidity"],
    df["Radiation"],
    alpha=0.3,
    s=10
)

plt.title("Humidity vs Solar Radiation")
plt.xlabel("Humidity")
plt.ylabel("Solar Radiation")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("humidity_vs_radiation.png", dpi=300)
plt.show()
# Correlation analysis
print("\nCorrelation with Solar Radiation:")

correlations = df[
    ["Radiation", "Temperature", "Humidity", "Pressure", "Speed"]
].corr()

print(correlations["Radiation"].sort_values(ascending=False))
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(9, 6))

sns.heatmap(
    correlations,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1,
    vmax=1
)

plt.title("Correlation Heatmap of Solar Radiation Variables")
plt.tight_layout()

plt.savefig("correlation_heatmap.png", dpi=300)
plt.show()