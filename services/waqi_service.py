import requests
import os
TOKEN = os.getenv("TOKEN")

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
    }