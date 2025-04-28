def crop_suitability(crop_row, climate_df):
    #Year
    ann_rain = climate_df["rain"].sum()

    #Filter months from sowing to harvesting
    if crop_row.sow_month <= crop_row.harvest_month:
        active_months = climate_df.

    #Monthly avarage
    monthly_match = (
        (climate_df["tmin"] >= crop_row["t_min"]) &
        (climate_df["tmax"] <= crop_row["t_max"])
    ).mean()

    rain_ok = crop_row["rain"]