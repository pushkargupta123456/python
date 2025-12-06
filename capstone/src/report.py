import os


def save_cleaned_data(df, filename="output/cleaned_energy_data.csv"):
    """Save the final processed data to CSV."""
    os.makedirs("output", exist_ok=True)
    df.to_csv(filename, index=False)
    print("✅ Saved cleaned data to", filename)


def save_building_summary(summary_df, filename="output/building_summary.csv"):
    """Save building-wise summary to CSV."""
    os.makedirs("output", exist_ok=True)
    summary_df.to_csv(filename)
    print("✅ Saved building summary to", filename)


def write_text_summary(df, building_summary, daily_totals, weekly_totals,
                        filename="output/summary.txt"):
    """Write a simple text summary of the analysis."""

    os.makedirs("output", exist_ok=True)

    total_campus_consumption = df["kWh"].sum()

    # Highest-consuming building
    highest_building = building_summary["sum"].idxmax()
    highest_building_value = building_summary.loc[highest_building, "sum"]

    # Peak load time (row where kWh is maximum)
    peak_index = df["kWh"].idxmax()
    peak_row = df.loc[peak_index]
    peak_time = peak_row["Timestamp"]
    peak_kwh = peak_row["kWh"]

    with open(filename, "w") as f:
        f.write("Campus Energy Usage Summary\n")
        f.write("---------------------------\n")
        f.write(f"Total campus consumption: {total_campus_consumption} kWh\n")
        f.write(f"Highest-consuming building: {highest_building} "
                f"({highest_building_value} kWh)\n")
        f.write(f"Peak load time: {peak_time} "
                f"with {peak_kwh} kWh\n\n")

        f.write("Daily Trend:\n")
        f.write(f"- Number of days recorded: {len(daily_totals)}\n")

        f.write("Weekly Trend:\n")
        f.write(f"- Number of weeks recorded: {len(weekly_totals)}\n")

    print("✅ Saved summary report to", filename)