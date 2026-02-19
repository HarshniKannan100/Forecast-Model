from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


def find_nearest_station(user_lat, user_lon, stations_df):
    stations_df["distance"] = stations_df.apply(
        lambda row: haversine(
            user_lat, user_lon,
            row["latitude"], row["longitude"]
        ),
        axis=1
    )

    nearest = stations_df.loc[stations_df["distance"].idxmin()]
    return nearest