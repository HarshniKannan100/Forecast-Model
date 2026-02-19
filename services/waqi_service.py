from datetime import datetime
import pandas as pd
import requests
import os
TOKEN = "5d884a451880e821b8e4c7ed3a8727ce0eb30650"

def fetch_station_coordinates(station_name: str):
    url = f"https://api.waqi.info/search/?token={TOKEN}&keyword={station_name}"

    res = requests.get(url).json()

    if res["status"] != "ok" or len(res["data"]) == 0:
        return None

    first = res["data"][0]

    lat = first["station"]["geo"][0]
    lon = first["station"]["geo"][1]

    return lat, lon

def fetch_live_aqi(lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={TOKEN}"

    res = requests.get(url).json()

    if res["status"] != "ok":
        return None

    data = res["data"]
    iaqi = data.get("iaqi", {})

    return {
        "aqi": data.get("aqi"),
        "pm25": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "so2": iaqi.get("so2", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v"),
        "co": iaqi.get("co", {}).get("v"),
    }

def cigarettes_last_7_days(station_df, live_data):

    # sort history
    station_df = station_df.sort_values("datetime")

    # 27 historical + live
    hist_last = station_df.tail(27)

    live_row = pd.DataFrame([{
        "pm25": live_data["pm25"],
        "datetime": datetime.now()
    }])

    last7 = pd.concat([hist_last, live_row])

    # average PM2.5
    avg_pm25 = last7["pm25"].mean()

    # cigarettes per day
    cigs_day = avg_pm25 / 22

    # weekly cigarettes
    cigs_week = cigs_day * 7

    return round(cigs_day, 1), round(cigs_week, 1)