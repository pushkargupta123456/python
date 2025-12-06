import matplotlib.pyplot as plt


def create_dashboard(df, daily_totals, weekly_totals, weekly_building_avg):
    """
    Make one figure with 3 plots and save as output/dashboard.png
    - Line: daily totals
    - Bar: average weekly per building
    - Scatter: all readings over time
    """

    print("🔹 Task 4: Creating dashboard.png")

    # Make sure df has Timestamp as index (for scatter plot)
    df2 = df.copy()
    df2 = df2.set_index("Timestamp")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # 1) Trend Line – daily consumption over time
    axes[0].plot(daily_totals.index, daily_totals.values)
    axes[0].set_title("Daily Consumption (All Buildings)")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("kWh")

    # 2) Bar Chart – average weekly usage across buildings
    axes[1].bar(weekly_building_avg.index, weekly_building_avg.values)
    axes[1].set_title("Average Weekly Usage per Building")
    axes[1].set_xlabel("Building")
    axes[1].set_ylabel("kWh (avg per week)")

    # 3) Scatter Plot – consumption vs time (points show peaks)
    axes[2].scatter(df2.index, df2["kWh"])
    axes[2].set_title("Consumption Over Time (Scatter)")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("kWh")

    plt.tight_layout()
    plt.savefig("output/dashboard.png")
    plt.close(fig)

    print("✅ Saved: output/dashboard.png")