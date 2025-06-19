import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from pathlib import Path

# === Paths ===
ROOT = Path(__file__).resolve().parents[2]
log_path = ROOT / "data" / "raw" / "vehicle_log.csv"
avg_speed_path = ROOT / "data" / "processed" / "avg_speed_by_route_hour.csv"

# === Load Data ===
@st.cache_data
def load_vehicle_log():
    df = pd.read_csv(log_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

@st.cache_data
def load_avg_speed():
    return pd.read_csv(avg_speed_path)

vehicle_df = load_vehicle_log()
avg_speed_df = load_avg_speed()

# === Sidebar Filters ===
st.sidebar.title("Filters")

routes = avg_speed_df["route_short_name"].sort_values().unique().tolist()
selected_route = st.sidebar.selectbox("Select a Route", routes)

hours = avg_speed_df["hour"].unique().tolist()
selected_hour = st.sidebar.selectbox("Select Hour of Day", sorted(hours))

# === Header ===
st.title("BP Traffic Insights Dashboard")
st.markdown("Real-time transit visualization for Budapest")

# === Section: Average Speed Trend ===
st.subheader("Average Speed by Route & Hour")
filtered_speed = avg_speed_df[
    (avg_speed_df["route_short_name"] == selected_route)
    & (avg_speed_df["hour"] == selected_hour)
]

if not filtered_speed.empty:
    st.metric(label=f"Avg Speed for Route {selected_route} at Hour {selected_hour}", 
              value=f"{filtered_speed['speed'].values[0]:.2f} km/h")
else:
    st.warning("No speed data available for this selection.")

# === Section: Live Vehicle Map ===
st.subheader("Live Vehicle Positions")

# Latest timestamp in the dataset
latest_time = vehicle_df['timestamp'].max()
latest_data = vehicle_df[vehicle_df['timestamp'] == latest_time]

# Optional filter by route
latest_data = latest_data[latest_data["route_id"].notna()]
latest_data = latest_data[latest_data["route_id"].astype(str).str.startswith(selected_route[:2])]

# Create Folium map
m = folium.Map(location=[47.4979, 19.0402], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

for _, row in latest_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=(
            f"Vehicle ID: {row['vehicle_id']}<br>"
            f"Route: {row['route_id']}<br>"
            f"Speed: {row['speed']:.2f} km/h"
        ),
        icon=folium.Icon(color="blue", icon="bus", prefix="fa")
    ).add_to(marker_cluster)

# Display map
st_data = st_folium(m, width=700, height=500)

# === Raw Data Option ===
with st.expander("Show Raw Data"):
    st.write(latest_data.head())

