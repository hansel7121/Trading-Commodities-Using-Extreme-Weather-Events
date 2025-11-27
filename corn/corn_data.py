import requests
import pandas as pd
from datetime import datetime, timedelta


def get_corn_data(lat, lon, years=10):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    print(f"Fetching Corn Belt data (Lat: {lat}, Lon: {lon})...")

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
        print(f"Error parsing data: {e}")
        return None


LAT_CORN_BELT = 42.03
LON_CORN_BELT = -93.64

df_corn = get_corn_data(LAT_CORN_BELT, LON_CORN_BELT)

if df_corn is not None:
    filename = "iowa_corn_temps_10y.csv"
    df_corn.to_csv(filename)