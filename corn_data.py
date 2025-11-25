import requests
import pandas as pd
from datetime import datetime, timedelta


def get_corn_data(lat, lon, years=10):
    # 1. Setup Dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    print(f"Fetching Corn Belt data (Lat: {lat}, Lon: {lon})...")

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


# --- Configuration for US Corn Belt (Iowa) ---
# Coordinates for central Iowa (Top corn producing state)
LAT_CORN_BELT = 42.03
LON_CORN_BELT = -93.64

df_corn = get_corn_data(LAT_CORN_BELT, LON_CORN_BELT)

if df_corn is not None:
    filename = "iowa_corn_temps_10y.csv"
    df_corn.to_csv(filename)

    print("-" * 30)
    print(f"Success! Data saved to {filename}")
    print("-" * 30)

    # --- Extreme Condition Analysis for Corn ---
    print("\nEXTREME CORN WEATHER ANALYSIS:")

    # 1. Heat Stress (Pollination Failure)
    # Month 7, 8 (July, August) | Temp > 34°C
    heat_stress = df_corn[
        (df_corn.index.month.isin([7, 8])) & (df_corn["Max_Temp_C"] > 34)
    ]

    # 2. Frost Damage (Kill Risk)
    # Month 5 (May - Late Spring), 9 (Sept - Early Fall) | Temp < 0°C
    frost_risk = df_corn[
        (df_corn.index.month.isin([5, 9])) & (df_corn["Min_Temp_C"] < 0)
    ]

    print(f"Days with Dangerous Heat (>34°C in Jul/Aug): {len(heat_stress)}")
    print(f"Days with Dangerous Frost (<0°C in May/Sept): {len(frost_risk)}")

    if len(heat_stress) > 0:
        print("\nRecent Heat Stress Dates:")
        print(heat_stress.tail(5).index.date)

    if len(frost_risk) > 0:
        print("\nRecent Frost Risk Dates:")
        print(frost_risk.tail(5).index.date)
