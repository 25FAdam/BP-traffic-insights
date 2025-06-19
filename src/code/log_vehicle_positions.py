import requests
import csv
import datetime
import os
from google.transit import gtfs_realtime_pb2

# Insert your BKK API key here
API_KEY = "YOUR_KEY_HERE"

# GTFS-RT Vehicle Positions endpoint
url = f"https://go.bkk.hu/api/query/v1/ws/gtfs-rt/full/VehiclePositions.pb?key={API_KEY}"

# Define the relative path to the output CSV file
CSV_FILE = os.path.join(os.path.dirname(__file__), "../../data/raw/vehicle_log.csv")

def fetch_gtfs_rt():
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    return feed

def save_to_csv(feed):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp", "vehicle_id", "route_id", "trip_id",
                "latitude", "longitude", "speed"
            ])
        for entity in feed.entity:
            vehicle = entity.vehicle
            writer.writerow([
                timestamp,
                vehicle.vehicle.id,
                vehicle.trip.route_id,
                vehicle.trip.trip_id,
                vehicle.position.latitude,
                vehicle.position.longitude,
                vehicle.position.speed
            ])
    print(f"✅ Logged {len(feed.entity)} vehicles at {timestamp}")

if __name__ == "__main__":
    feed = fetch_gtfs_rt()
    if feed:
        save_to_csv(feed)
