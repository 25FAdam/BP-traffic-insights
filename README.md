Status: Currently under development. Features are being added iteratively.

# Budapest Intelligent Traffic Insight System (BITIS)

An open-source system that visualizes, simulates, and predicts public transportation and traffic flow in Budapest using real-time APIs and machine learning.

## Features

### Real-Time Data Integration
- Integrates GTFS real-time (RT) feeds from BKK to track live positions of trams, buses, and metros.

### Interactive Map Dashboard
- Visualizes transit routes and live vehicle locations on an interactive map.
- Highlights areas of high congestion or unusual delays.

### Historical Analysis
- Processes and analyzes historical GTFS data.
- Generates trends of average delay per line, route, or district.

### Anomaly Detection
- Applies machine learning techniques (e.g., Isolation Forest, clustering) to detect unusual delays or route disruptions.
- Flags deviations from historical norms.

## Project Structure

...

## Getting Started
```bash
git clone https://github.com/25FAdam/BP-traffic-insights.git
cd BP-traffic-insights
python -m venv venv
pip install -r requirements.txt