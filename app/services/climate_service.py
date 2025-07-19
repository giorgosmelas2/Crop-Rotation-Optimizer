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
        "month": list(range(1, 13)),
        "tmin": [js["T2M_MIN"].get(m, 0.0) for m in MONTH_ORDER],
        "tmax": [js["T2M_MAX"].get(m, 0.0) for m in MONTH_ORDER],
        "rain": [js["PRECTOTCORR"].get(m, 0.0) for m in MONTH_ORDER],
        "evap": [js["EVPTRNS"].get(m, 0.0) for m in MONTH_ORDER],   
        "rh":   [js["RH2M"].get(m, 0.0) for m in MONTH_ORDER],      
    })
        
    climate = Climate.from_dataframe(df)
    
    return climate