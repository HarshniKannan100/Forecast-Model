import requests

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
    response = requests.get(url).json()

    if response["status"] == "ok":
        return response["data"]["aqi"]
    else:
        return None
    
