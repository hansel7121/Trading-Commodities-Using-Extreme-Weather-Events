import requests
import pandas as pd
from datetime import datetime, timedelta


def get_soybean_data(lat, lon, years=10):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    print(f"Fetching data for US Soybean Belt (Lat: {lat}, Lon: {lon})...")
    print(f"Period: {start_date.date()} to {end_date.date()}")

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

    try:
        properties = data["properties"]["parameter"]
        df_max = pd.Series(properties["T2M_MAX"], name="Max_Temp_C")
        df_min = pd.Series(properties["T2M_MIN"], name="Min_Temp_C")

        df = pd.concat([df_max, df_min], axis=1)

        df.index = pd.to_datetime(df.index, format="%Y%m%d")
        df.index.name = "Date"

        df = df[df["Max_Temp_C"] > -100]

        return df

    except KeyError as e:
        print(f"Error parsing data structure: {e}")
        return None

LAT_SOYBEAN_BELT = 41.58
LON_SOYBEAN_BELT = -93.62

df_soy = get_soybean_data(LAT_SOYBEAN_BELT, LON_SOYBEAN_BELT)

if df_soy is not None:
    filename = "iowa_soybean_temps_10y.csv"
    df_soy.to_csv(filename)
