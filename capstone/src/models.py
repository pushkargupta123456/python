class MeterReading:
    """Simple object to store one meter reading."""

    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    """Represents one building and all its meter readings."""

    def __init__(self, name):
        self.name = name
        self.meter_readings = []   # list of MeterReading objects

    def add_reading(self, timestamp, kwh):
        reading = MeterReading(timestamp, kwh)
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        total = 0
        for r in self.meter_readings:
            total += r.kwh
        return total

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building: {self.name}, Total Consumption: {total} kWh"


class BuildingManager:
    """Keeps track of many buildings."""

    def __init__(self):
        self.buildings = {}   # key: building name, value: Building object

    def add_reading_from_row(self, building_name, timestamp, kwh):
        # Create building if not present
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)

        # Add reading to that building
        self.buildings[building_name].add_reading(timestamp, kwh)

    def load_from_dataframe(self, df):
        """
        Take the combined dataframe and fill all Building objects.
        Expects columns: Building, Timestamp, kWh
        """
        for _, row in df.iterrows():
            self.add_reading_from_row(
                row["Building"],
                row["Timestamp"],
                row["kWh"]
            )

    def print_reports(self):
        for b in self.buildings.values():
            print(b.generate_report())