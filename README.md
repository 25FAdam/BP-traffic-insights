# ------WORK IN PROGRESS------

# Budapest Intelligent Traffic Insight System (BITIS)

An open-source system that visualizes, simulates, and predicts public transportation and traffic flow in Budapest using real-time APIs and machine learning.

## Features
- Real-time public transport data visualization (BKK FUTÁR API)
- Weather data integration (OpenWeatherMap API)
- Traffic pattern prediction with ML models
- Streamlit dashboard for interactive exploration

## Project Structure

```
.
├── data/ # Raw and processed data files
├── notebooks/ # EDA and model-building notebooks
├── src/ # Core source code (API, ML, etc.)
├── models/ # Trained models and pipeline outputs
├── dashboard/ # Streamlit frontend components
├── requirements.txt
└── README.md
```

## Getting Started
```bash
git clone https://github.com/25FAdam/BP-traffic-insights.git
cd BP-traffic-insights
python -m venv venv
pip install -r requirements.txt
