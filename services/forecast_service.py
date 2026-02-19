from datetime import datetime

def compute_baseline(station_df, month):
    baseline = station_df[
        station_df["month"] == month
    ].groupby("hour")["aqi"].mean()

    return baseline.sort_index()


def generate_24h_forecast(live_aqi, baseline):

    six_hour_baseline = baseline.values.tolist()
    nearest_hour = baseline.index[0]  # simple anchor

    baseline_current = baseline[nearest_hour]
    deviation = live_aqi - baseline_current

    six_hour_forecast = [live_aqi]

    for i in range(4):  # 24 hours
        base = six_hour_baseline[i % len(six_hour_baseline)]
        decay = 0.95 ** (i + 1)
        predicted = base + deviation * decay
        six_hour_forecast.append(predicted)

    return interpolate_hourly(six_hour_forecast)[1:25]


def generate_72h_forecast(live_aqi, baseline):

    six_hour_baseline = baseline.values.tolist()
    baseline_current = baseline.iloc[0]
    deviation = live_aqi - baseline_current

    forecast = []

    for i in range(12):  # 72 hours
        base = six_hour_baseline[i % len(six_hour_baseline)]
        decay = 0.95 ** (i + 1)
        predicted = base + deviation * decay
        forecast.append(predicted)

    return forecast


def interpolate_hourly(values):
    hourly = []

    for i in range(len(values) - 1):
        start = values[i]
        end = values[i+1]
        step = (end - start) / 6

        for h in range(6):
            hourly.append(start + step * h)

    hourly.append(values[-1])
    return hourly