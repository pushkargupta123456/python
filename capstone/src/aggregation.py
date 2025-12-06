import pandas as pd


def calculate_daily_totals(df):
    """
    Return total kWh for each day (all buildings combined).
    """

    print("🔹 Task 2: Calculating daily totals")

    # Work on a copy so we don't change original DF
    df2 = df.copy()

    # Set Timestamp as index for resample
    df2 = df2.set_index("Timestamp")

    # Sum kWh per day
    daily_totals = df2["kWh"].resample("D").sum()

    return daily_totals


def calculate_weekly_aggregates(df):
    """
    Return total kWh for each week (all buildings combined).
    """

    print("🔹 Task 2: Calculating weekly totals")

    df2 = df.copy()
    df2 = df2.set_index("Timestamp")

    weekly_totals = df2["kWh"].resample("W").sum()

    return weekly_totals


def building_wise_summary(df):
    """
    Return summary (mean, min, max, sum) for each building.
    """

    print("🔹 Task 2: Calculating building-wise summary")

    summary = df.groupby("Building")["kWh"].agg(["mean", "min", "max", "sum"])

    return summary


def building_weekly_average(df):
    """
    Average weekly kWh for each building.
    This will be used for the bar chart in the dashboard.
    """

    print("🔹 Task 2: Calculating average weekly usage per building")

    df2 = df.copy()
    df2 = df2.set_index("Timestamp")

    # First: weekly totals per building
    weekly_building = df2.groupby("Building")["kWh"].resample("W").sum()
    weekly_building = weekly_building.reset_index()   # columns: Building, Timestamp, kWh

    # Now: average weekly kWh for each building
    weekly_avg = weekly_building.groupby("Building")["kWh"].mean()

    return weekly_avg