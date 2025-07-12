import requests, pandas as pd
from app.models.coordinates import Coordinates 
from app.ml.core_models.climate import Climate

BASE_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"
PARAMS   = "T2M_MIN,T2M_MAX,PRECTOTCORR,EVPTRNS,RH2M"
MONTH_ORDER = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

def get_climate_data(
    coordinates: Coordinates, 
    start_year: int = 2015, 
    end_year: int = 2024
    ) -> Climate:

    params = {
        "parameters": PARAMS,
        "community": "AG", 
        "latitude": coordinates.lat,
        "longitude": coordinates.lng,
        "format": "JSON",
        "start": start_year,
        "end": end_year
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    js = response.json()["properties"]["parameter"]

    #Use monthes that exists in the response
    months = [m for m in MONTH_ORDER if m in js["T2M_MIN"]]

    df = pd.DataFrame({
        "month": list(range(1,13)),
        "tmin": [js["T2M_MIN"][m] for m in months],
        "tmax": [js["T2M_MAX"][m] for m in months],
        "rain": [js["PRECTOTCORR"][m] for m in months],
        "evap": [js["EVPTRNS"][m] for m in months],
        "rh": [js["RH2M"][m] for m in months],
    })
    
    climate = Climate.from_dataframe(df)

    return climate