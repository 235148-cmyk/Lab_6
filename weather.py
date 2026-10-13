
import pandas as pd
import matplotlib.pyplot as plt

raw = {
    "Date": [
        "2026-09-01", "2026-09-02", "2026-09-03",
        "2026-09-04", "2026-09-05", "2026-09-06",
        "2026-09-07", "2026-09-08", "2026-09-09",
        "2026-09-10", "2026-09-11", "2026-09-12",
        "2026-09-13", "2026-09-14", "2026-09-15"
    ],
    "City": [
        " lahore", "ISLAMABAD ", "Karachi", "lahore ",
        "Islamabad", "KARACHI", "Lahore", "islamabad",
        " Karachi", "LAHORE", "Islamabad ", "KARACHI",
        " lahore ", "ISLAMABAD", "karachi "
    ],
    "Temperature": [
        "32C", "29C", "34C", "27C", "28C",
        "35C", "30C", "26C", "33C", "31C",
        "29C", "25C", "28C", "30C", "34C"
    ],
    "Humidity": [
        45, 50, None, 55, 60,
        65, None, 58, 62, 70,
        48, None, 66, 52, 59
    ],
    "Condition": [
        " sunny", "CLOUDY ", "Sunny", " Rainy",
        "cloudy", "SUNNY ", "Cloudy", "RAINY",
        " sunny ", "CLOUDY", "Sunny", " rainy ",
        "Cloudy ", "SUNNY", "Sunny"
    ]
}

df = pd.DataFrame(raw)

df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

print("Original Dataset:")
print(df)

df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()

df["Temperature"] = (
    df["Temperature"]
    .str.replace("C", "", regex=False)
)
df["Temperature"] = pd.to_numeric(
    df["Temperature"], errors="coerce"
)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df = df.drop_duplicates().reset_index(drop=True)

print("\nRows after dropping duplicates:", len(df))

humidity_median = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(humidity_median)

print("Missing Humidity filled with median:",
      humidity_median)

condition_encoded = pd.get_dummies(
    df["Condition"],
    prefix="Condition",
    dtype=int
)

print("\nEncoded Condition Columns:")
print(condition_encoded.head().to_string(index=False))

condition_counts = df["Condition"].value_counts()
correlation = df["Temperature"].corr(df["Humidity"])

print("\nCorrelation (Temperature, Humidity):",
      round(correlation, 3))

print("\nCondition counts:")
print(condition_counts)

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(
    df["Date"], df["Temperature"],
    marker="o", label="Temperature"
)
axes[0, 0].set_title("Temperature Over Time")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (C)")
axes[0, 0].tick_params(axis="x", rotation=30)
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(
    df["Temperature"], df["Humidity"]
)
axes[0, 1].set_title("Temperature vs Humidity")
axes[0, 1].set_xlabel("Temperature (C)")
axes[0, 1].set_ylabel("Humidity (%)")
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].pie(
    condition_counts.values,
    labels=condition_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 0].set_title("Weather Condition Share")

axes[1, 1].hist(
    df["Temperature"],
    bins=5,
    edgecolor="black"
)
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()

plt.savefig("weather_dashboard.png", dpi=150)
print("\nSaved weather_dashboard.png")

plt.show()
