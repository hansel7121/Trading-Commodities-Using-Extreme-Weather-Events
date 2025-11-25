import requests
import pandas as pd
from datetime import datetime, timedelta


def get_weather_data(lat, lon, years=10):
    # 1. Setup Dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    print(f"Fetching Wheat Belt data (Lat: {lat}, Lon: {lon})...")

    # 2. NASA POWER API Config
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M_MAX,T2M_MIN",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_str,
        "end": end_str,
        "format": "JSON",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    # 3. Process Data
    try:
        properties = data["properties"]["parameter"]
        df_max = pd.Series(properties["T2M_MAX"], name="Max_Temp_C")
        df_min = pd.Series(properties["T2M_MIN"], name="Min_Temp_C")

        df = pd.concat([df_max, df_min], axis=1)
        df.index = pd.to_datetime(df.index, format="%Y%m%d")
        df.index.name = "Date"

        # Filter out NASA error codes (-999)
        df = df[df["Max_Temp_C"] > -100]
        return df

    except KeyError as e:
        print(f"Error parsing data: {e}")
        return None


# --- Configuration for US Wheat Belt (Kansas) ---
# Coordinates for Central Kansas (Major Winter Wheat producer)
LAT_WHEAT_BELT = 38.50
LON_WHEAT_BELT = -98.20

df_wheat = get_weather_data(LAT_WHEAT_BELT, LON_WHEAT_BELT)

if df_wheat is not None:
    filename = "kansas_wheat_temps_10y.csv"
    df_wheat.to_csv(filename)

    print("-" * 30)
    print(f"Success! Data saved to {filename}")
    print("-" * 30)

    # --- Extreme Condition Analysis for Winter Wheat ---
    print("\nEXTREME WHEAT WEATHER ANALYSIS:")

    # 1. Heat Stress (Grain Fill & Maturation)
    # Critical Period: May (5) and June (6)
    # Danger: Temps > 32°C (90°F) cause shriveled grain and yield loss
    heat_stress = df_wheat[
        (df_wheat.index.month.isin([5, 6])) & (df_wheat["Max_Temp_C"] > 32)
    ]

    # 2. Spring Freeze (The "Widowmaker")
    # Critical Period: April (4) and May (5)
    # Danger: Temps < -2°C (28°F) when the wheat head is emerging (Jointing/Heading)
    # Note: Wheat is fine in winter, but vulnerable once it starts growing in Spring.
    frost_risk = df_wheat[
        (df_wheat.index.month.isin([4, 5])) & (df_wheat["Min_Temp_C"] < -2)
    ]

    print(f"Days with Dangerous Heat (>32°C in May/Jun): {len(heat_stress)}")
    print(f"Days with Spring Freeze (< -2°C in Apr/May): {len(frost_risk)}")

    if len(heat_stress) > 0:
        print("\nRecent Heat Stress Dates:")
        print(heat_stress.tail(5).index.date)

    if len(frost_risk) > 0:
        print("\nRecent Spring Freeze Dates:")
        print(frost_risk.tail(5).index.date)
