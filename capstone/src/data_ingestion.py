import os
import pandas as pd


def load_and_merge_csv(data_folder="data"):
    """Read all CSV files from the data folder and combine them."""

    print("🔹 Task 1: Reading CSV files from folder:", data_folder)

    all_dfs = []          # list to store dataframes
    csv_files = []        # list of filenames

    # Find all .csv files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            csv_files.append(filename)

    if not csv_files:
        print("No CSV files found in the data folder.")
        return None

    # Read each CSV file
    for filename in csv_files:
        file_path = os.path.join(data_folder, filename)
        print("Reading:", file_path)

        try:
            df = pd.read_csv(file_path)

            # Add Building name from file name if not present
            if "Building" not in df.columns:
                building_name = filename.replace(".csv", "")
                df["Building"] = building_name

            # Make sure Timestamp is a datetime
            if "Timestamp" in df.columns:
                df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
                df = df.dropna(subset=["Timestamp"])
            else:
                print("  ⚠️ No 'Timestamp' column in", filename)
                continue

            # Make sure kWh is numeric
            if "kWh" in df.columns:
                df["kWh"] = pd.to_numeric(df["kWh"], errors="coerce")
                df = df.dropna(subset=["kWh"])
            else:
                print("  ⚠️ No 'kWh' column in", filename)
                continue

            all_dfs.append(df)

        except Exception as e:
            # Handle corrupt file
            print("  ❌ Could not read file:", filename)
            print("     Error:", e)

    if not all_dfs:
        print("No valid data loaded.")
        return None

    # Combine all dataframes into one
    combined_df = pd.concat(all_dfs, ignore_index=True)
    print("✅ Combined data shape:", combined_df.shape)

    return combined_df