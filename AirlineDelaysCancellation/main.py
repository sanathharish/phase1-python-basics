import pandas as pd
from datetime import datetime
import os

# ----------------------------
# Utility Functions
# ----------------------------
def log_action(filename, message):
    """Append a timestamped message to the given log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

# ----------------------------
# Setup Folders
# ----------------------------
os.makedirs("Logs", exist_ok=True)
os.makedirs("CleanData", exist_ok=True)

# ----------------------------
# Load Datasets
# ----------------------------
airline = pd.read_csv("./RawData/airlines.csv")
airports = pd.read_csv("./RawData/airports.csv")
flights = pd.read_csv(
    "./RawData/flights.csv",
    dtype={"ORIGIN_AIRPORT": str, "DESTINATION_AIRPORT": str},
    low_memory=False
)

# ----------------------------
# Handle Missing Coordinates (Airports)
# ----------------------------
missing_airports = airports[airports[['LATITUDE', 'LONGITUDE']].isnull().any(axis=1)]
missing_codes = missing_airports['IATA_CODE'].tolist()

# Save missing airports to log
missing_airports_path = "Logs/missing_airports.txt"
missing_airports.to_csv(missing_airports_path, sep='\t', index=False)
log_action("Logs/cleaning_log.txt",
           f"Identified {len(missing_airports)} airports with missing coordinates. Saved to {missing_airports_path}")

# Drop rows with missing coordinates
airports = airports.dropna(subset=['LATITUDE', 'LONGITUDE'])
log_action("Logs/cleaning_log.txt", "Dropped airports with missing LAT/LONG values.")

# ----------------------------
# Remove Flights Linked to Missing Airports
# ----------------------------
mask = (
    flights['ORIGIN_AIRPORT'].isin(missing_codes) |
    flights['DESTINATION_AIRPORT'].isin(missing_codes)
)
dropped_flights = flights[mask]

# Save dropped flight records
dropped_flights_path = "Logs/dropped_flights_due_to_missing_airports.txt"
dropped_flights.to_csv(dropped_flights_path, sep='\t', index=False)

# Drop from main dataset
flights = flights[~mask]

log_action(
    "Logs/cleaning_log.txt",
    f"Dropped {len(dropped_flights)} flights linked to missing airports. Saved details to {dropped_flights_path}"
)

# ----------------------------
# ✅ Save Cleaned Datasets (Optional but Recommended)
# ----------------------------
airline.to_csv("CleanData/airlines_cleaned.csv", index=False)
airports.to_csv("CleanData/airports_cleaned.csv", index=False)
flights.to_csv("CleanData/flights_cleaned.csv", index=False)

log_action("Logs/cleaning_log.txt", "Saved cleaned datasets to CleanData folder.")

print("\n✅ Data Cleaning Complete!")
print(f"🛫 Dropped {len(missing_airports)} airports and {len(dropped_flights)} flights due to missing coordinates.")
print("💾 Cleaned files saved in: CleanData/")
print("📜 Logs available in: Logs/")
