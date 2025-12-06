# -------------------------------------------------------
# WEATHER DATA VISUALIZER – MAIN SCRIPT (READY TO RUN)
# -------------------------------------------------------
# Requirements: pandas, numpy, matplotlib
# Install if needed:
# pip install pandas numpy matplotlib
# -------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================
# TASK 1: DATA LOADING
# ============================

df = pd.read_csv("weather.csv")  # <-- put your dataset in same folder
print("\n----- HEAD -----\n", df.head())
print("\n----- INFO -----\n")
print(df.info())
print("\n----- STATISTICS -----\n", df.describe())

# ============================
# TASK 2: DATA CLEANING
# ============================

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Handle missing values
df.fillna(method="ffill", inplace=True)     # Forward-fill missing values

# Select necessary columns (update column names if different)
df = df[["Date", "Temperature", "Humidity", "Rainfall"]]

# Export cleaned dataset
df.to_csv("cleaned_weather.csv", index=False)
print("\nCLEANED DATA SAVED → cleaned_weather.csv\n")

# ============================
# TASK 3: NUMPY STATISTICS
# ============================

temp = df["Temperature"].values

print("\n--- WEATHER STATISTICS USING NUMPY ---")
print("Mean Temperature :", np.mean(temp))
print("Maximum Temp     :", np.max(temp))
print("Minimum Temp     :", np.min(temp))
print("Std Deviation    :", np.std(temp))

# ============================
# TASK 4: VISUALIZATION
# ============================

os.makedirs("plots", exist_ok=True)  # Folder to store images

# 1) Line Chart - Daily Temperature
plt.figure(figsize=(10,5))
plt.plot(df["Date"], df["Temperature"])
plt.xlabel("Date"); plt.ylabel("Temperature (°C)")
plt.title("Daily Temperature Trend")
plt.savefig("plots/daily_temperature.png")
plt.close()

# 2) Bar Chart - Monthly Rainfall
df["Month"] = df["Date"].dt.month
monthly_rain = df.groupby("Month")["Rainfall"].sum()

plt.figure(figsize=(10,5))
plt.bar(monthly_rain.index, monthly_rain.values)
plt.xlabel("Month"); plt.ylabel("Rainfall (mm)")
plt.title("Monthly Rainfall")
plt.savefig("plots/monthly_rainfall.png")
plt.close()

# 3) Scatter Plot - Temperature vs Humidity
plt.figure(figsize=(8,5))
plt.scatter(df["Temperature"], df["Humidity"])
plt.xlabel("Temperature (°C)"); plt.ylabel("Humidity (%)")
plt.title("Humidity vs Temperature")
plt.savefig("plots/humidity_vs_temp.png")
plt.close()

# 4) Combined Subplot
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(df["Date"], df["Temperature"])
plt.title("Temperature Trend")

plt.subplot(1,2,2)
plt.scatter(df["Temperature"], df["Humidity"])
plt.title("Temp vs Humidity")

plt.savefig("plots/combined.png")
plt.close()

print("\nAll Visual Graphs Saved Inside /plots Folder ✔")

# ============================
# TASK 5: GROUP & ANALYSIS
# ============================

grouped = df.groupby("Month").agg({
    "Temperature": "mean",
    "Humidity": "mean",
    "Rainfall": "sum"
})

print("\nMONTHLY WEATHER SUMMARY:\n", grouped)

# ============================
# TASK 6: AUTO REPORT GENERATION
# ============================

with open("REPORT.md","w") as file:
    file.write("# WEATHER ANALYSIS REPORT\n\n")
    file.write("## Key Insights:\n")
    file.write(f"- Average Temperature: {np.mean(temp)} °C\n")
    file.write(f"- Highest Recorded: {np.max(temp)} °C\n")
    file.write(f"- Lowest Recorded: {np.min(temp)} °C\n")
    file.write("\n## Monthly Summary:\n")
    file.write(str(grouped))
    file.write("\n\nGraphs Available in /plots Folder\n")

print("\nREPORT GENERATED → REPORT.md")
print("\n🎉 PROJECT COMPLETED SUCCESSFULLY!")