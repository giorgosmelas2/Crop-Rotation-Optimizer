import pandas as pd

from app.ml.core_models.crop import Crop

def climate_evaluation(climate_df: dict, crop: Crop) -> float:

    total_temperature_score = 0.0
    rain_score = 0.0

    sow = crop.sow_month
    harvest = crop.harvest_month

    if sow <= harvest: 
        active_temp = climate_df.iloc[sow:harvest][["tmin", "tmax"]]
    else:
        active_temp = pd.concat([
            climate_df.iloc[sow:][["tmin", "tmax"]],
            climate_df[:harvest][["tmin", "tmax"]]
        ])

    TOL = 4  # Tolerance for temperature
    months = len(active_temp)

    # Calculating temperature score
    t_min_deviation = (crop["t_min"] - active_temp["tmin"]).clip(lower=0)
    t_max_deviation = (active_temp["tmax"] - crop["t_max"]).clip(lower=0)

    # 1 if temperature is ok, <1 if is a little more, 0 if is not ok
    t_min_score = (1 - (t_min_deviation / TOL)).clip(lower=0)
    t_max_score = (1 - (t_max_deviation / TOL)).clip(lower=0)

    # Calculating optimal temperature score
    t_opt_min_deviation = (crop["t_opt_min"] - active_temp["tmin"]).clip(lower=0)
    t_opt_max_deviation = (active_temp["tmax"] - crop["t_opt_max"]).clip(lower=0)

    # 1 if temperature is ok, <1 if is a little more, 0 if is not ok
    t_opt_min_score = (1 - (t_opt_min_deviation / TOL)).clip(lower=0)
    t_opt_max_score = (1 - (t_opt_max_deviation / TOL)).clip(lower=0)

    temp_score = (t_min_score + t_max_score) / 2
    temperature_score = temp_score.mean() * 0.3 # Average of all months

    temp_opt_score = (t_opt_min_score + t_opt_max_score) / 2
    temperature_opt_score = temp_opt_score.mean() * 0.7  # Average of all months

    total_temperature_score = temperature_score + temperature_opt_score

    # Calculating rainfall score
    if sow <= harvest: 
        active_rain = climate_df.iloc[sow:harvest][["rain"]]
    else :
        active_rain = pd.concat([
            climate_df.iloc[sow:][["rain"]],
            climate_df[:harvest][["rain"]]
        ])

    months = active_rain.index.tolist()
    for month in months:
        if month < 7 and month % 2 == 0 and month != 0:
            active_rain[month] *= 30
        elif month <= 7 and month % 2 != 0:
            active_rain[month] *= 31
        elif month > 7 and month % 2 == 0:
            active_rain[month] *= 31
        elif month > 7 and month % 2 != 0:
            active_rain[month] *= 30    
        else: 
            active_rain[month] *= 28

    rain_per_month = crop["rain_min"] / months
    rain_deviation_percent = (active_rain["rain"] - rain_per_month / rain_per_month) * 100
    avg_rain_deviation = abs(rain_deviation_percent.mean())

    if avg_rain_deviation <= 0.1:
        rain_score = 1.0
    elif avg_rain_deviation <= 0.2:
        rain_score = 0.9
    elif avg_rain_deviation <= 0.3:
        rain_score = 0.8
    elif avg_rain_deviation <= 0.5:
        rain_score = 0.4
    else: 
        rain_score = 0.0
    
