import requests, pandas as pd, datetime as dt

BASE_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"
PARAMS   = "T2M_MIN,T2M_MAX,PRECTOTCORR"
MONTH_ORDER = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

def get_climatology(lat: float, lon: float) -> pd.DataFrame:
    params = {
        "parameters": PARAMS,
        "community":  "AG",
        "latitude":   lat,
        "longitude":  lon,
        "format":     "JSON"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    js = response.json()["properties"]["parameter"]

    #Use monthes that exists in the response
    months = [m for m in MONTH_ORDER if m in js["T2M_MIN"]]

    df = pd.DataFrame({
        "tmin": [js["T2M_MIN"][m] for m in months],
        "tmax": [js["T2M_MAX"][m] for m in months],
        "rain": [js["PRECTOTCORR"][m] for m in months],
    })

    return df