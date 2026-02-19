from fastapi import FastAPI
from datetime import datetime
import pandas as pd
from services.geo_utils import find_nearest_station
from services.forecast_service import (
    compute_baseline,
    generate_24h_forecast,
    generate_72h_forecast
)
from services.waqi_service import fetch_station_coordinates, fetch_live_aqi, cigarettes_last_7_days
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # temporary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load dataset once
df = pd.read_csv("data/aqi_dataset.csv")

stations_df = df[["latitude", "longitude"]].drop_duplicates()


@app.get("/forecast")
def forecast(station: str):

    coords = fetch_station_coordinates(station)

    if coords is None:
        return {"error": "Station not found"}

    lat, lon = coords

    nearest = find_nearest_station(lat, lon, stations_df)

    station_df = df[
        (df["latitude"] == nearest["latitude"]) &
        (df["longitude"] == nearest["longitude"])
    ]


    current_month = datetime.now().month
    live_data = fetch_live_aqi(lat, lon)

    current_aqi = live_data["aqi"]   # ⭐ extract number

    baseline = compute_baseline(station_df, current_month)

    forecast_24h = generate_24h_forecast(current_aqi, baseline)
    forecast_72h = generate_72h_forecast(current_aqi, baseline)
    cigs_7d = cigarettes_last_7_days(station_df,live_data)

    return {
    "station": station,
    "current": live_data,   # full dict
    "forecast_24h": forecast_24h,
    "forecast_72h": forecast_72h,
    "cigarettes_7d": cigs_7d 
    }  