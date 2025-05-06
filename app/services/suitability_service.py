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

    TOL = 4 #Tolerance for temperature
    months = len(active)

    #Calculating temperature score
    tmin_deviation = (crop_row["t_min"] - active["tmin"]).clip(lower=0)
    tmax_deviation = (active["tmax"] - crop_row["t_max"]).clip(lower=0)

    #1 if temperature is ok, <1 if is a little more, 0 if is not ok
    tmin_score = (1 - (tmin_deviation / TOL)).clip(lower=0)
    tmax_score = (1 - (tmax_deviation / TOL)).clip(lower=0)

    temp_score = (tmin_score + tmax_score) / 2
    temp_match_ratio = temp_score.mean() #Average of all months
    
    #Calculating rain score
    rain_scores = [
        rain_month_score(rain, crop_row["rain_min"] / months, crop_row["rain_max"] / months)
        for rain in active["rain"]
    ]
    rain_match = sum(rain_scores) / len(rain_scores)

    # Final score
    score = 0.7 * temp_match_ratio + 0.3 * rain_match
    return score

def rain_month_score (rain_value, rmin, rmax):
    if rmin <= rain_value <= rmax:
        return 1.0
    elif rain_value < rmin:
        return max(0.85, 1- (rmin - rain_value) / rmin)
    else:
        return max(0.75, 1 - (rain_value - rmax) / rmax)