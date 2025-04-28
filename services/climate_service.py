import requests, pandas as pd, datetime as dt

def get_monthly_climate(lat, lon):
    endpoint = (
        "https://power.larc.nasa.gov/api/temporal/monthly/point"
        f"?parameters=T2M_MIN,T2M_MAX,PRECTOT"
        f"&community=AG&longitude={lon}&latitude={lat}&format=JSON"
    )

    data = requests.get(endpoint, timeout=15).json()["properties"]["parameter"]
    df = pd.DataFrame({
        "tmin": data["T2M_MIN"].values(),
        "tmax": data["T2M_MAX"].values(),   
        "rain": data["PRECTOT"].values()
    })

    return df