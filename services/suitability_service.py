import pandas as pd

def crop_suitability(crop_row, climate_df):

    sow = crop_row["sow_month"] - 1 #iloc starts from 0 
    harvest = crop_row["harvest_month"] 

    #Filter months from sowing to harvesting
    if sow <= harvest:
        active = climate_df.iloc[sow : harvest]
    else:
        active = pd.concat([
            climate_df.iloc[sow:],
            climate_df[:harvest]
        ])



    #Monthly avarage
    monthly_match = (
        (climate_df["tmin"] >= crop_row["t_min"]) &
        (climate_df["tmax"] <= crop_row["t_max"])
    ).mean()

    temp_match_ratio = (
        (active["tmin"] >= crop_row["t_min"]) &
        (active["tmax"] <= crop_row["t_max"])
    ).mean()

    #Total rain from sowing month to harvest month
    total_rain = active["rain"].sum()
    rain_ok = crop_row["rain_min"] <= total_rain <= crop_row["rain_max"]

    score = temp_match_ratio * (1 if rain_ok else 0.5)
    return score