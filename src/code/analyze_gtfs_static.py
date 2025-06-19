from pathlib import Path
import pandas as pd

# ------------------------------------------------------------------
# 0.  Set paths
# ------------------------------------------------------------------
root       = Path(__file__).resolve().parents[2]
gtfs_path  = root / "data" / "raw" / "budapest_gtfs"
log_path   = root / "data" / "raw" / "vehicle_log.csv"

# ------------------------------------------------------------------
# 1.  Load GTFS static files
# ------------------------------------------------------------------
trips      = pd.read_csv(gtfs_path / "trips.txt")          # still useful later
routes     = pd.read_csv(gtfs_path / "routes.txt")

print("GTFS static loaded:",
      f"trips={len(trips):,}", f"routes={len(routes):,}", sep="\n  ")

# ------------------------------------------------------------------
# 2.  Load real-time log
# ------------------------------------------------------------------
vehicle_log = pd.read_csv(log_path)
vehicle_log["timestamp"] = pd.to_datetime(vehicle_log["timestamp"])

required_cols = {"timestamp", "vehicle_id", "route_id", "trip_id",
                 "latitude", "longitude", "speed"}
missing_cols  = required_cols - set(vehicle_log.columns)
if missing_cols:
    raise ValueError(f"'vehicle_log.csv' is missing columns: {missing_cols}")

print("\nvehicle_log sample:")
print(vehicle_log.head())

# ------------------------------------------------------------------
# 3.  Enrich with route_short_name (single merge)
# ------------------------------------------------------------------
merged = vehicle_log.merge(
    routes[["route_id", "route_short_name"]],
    how="left",
    on="route_id"
)

# How many route_ids had no match?
unmatched = merged["route_short_name"].isna().sum()
if unmatched:
    print(f"\n{unmatched} rows have route_id not found in routes.txt")

print("\nMerged sample (after adding route_short_name):")
print(merged[[
    "timestamp", "vehicle_id", "route_id",
    "route_short_name", "speed"
]].head())

# ------------------------------------------------------------------
# 4.  Aggregate: average speed by route & hour
# ------------------------------------------------------------------
merged["hour"] = merged["timestamp"].dt.hour

avg_speed = (
    merged.dropna(subset=["route_short_name", "speed"])
          .groupby(["route_short_name", "hour"])["speed"]
          .mean()
          .reset_index()
          .sort_values(["route_short_name", "hour"])
)

print("\nAverage speed by route & hour:")
print(avg_speed.head(10))

# ------------------------------------------------------------------
# 5.  Save results
# ------------------------------------------------------------------
out_dir  = root / "data" / "processed"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "avg_speed_by_route_hour.csv"
avg_speed.to_csv(out_path, index=False)
print(f"\n💾  Saved: {out_path}")
