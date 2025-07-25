from pydantic import BaseModel
import pandas as pd
from fastapi import APIRouter
from app.services.supabase_client import supabase
from app.models.coordinates import Coordinates
from app.ml.core_models.climate import Climate
from app.services.climate_service import get_climate_data
from app.services.suitability_service import crop_suitability

router = APIRouter()

@router.post("/suggest-crops")
async def suggest(req: Coordinates):
    climate = get_climate_data(req)
    climate_df = climate_to_dataframe(climate)

    crops = supabase.table("crops") \
        .select("crop_id, crop_name, sow_month, harvest_month") \
        .execute().data
    
    climates = supabase.table("crop_climate") \
        .select("crop_id, t_min, t_max, rain_min, rain_max") \
        .execute().data
    
    # Filter crops based on climate data
    rows = []
    for crop in crops:
        cc = next((cl for cl in climates if cl["crop_id"] == crop["crop_id"]), None)
        if cc:
            rows.append({
                "crop_id": crop["crop_id"],
                "crop_name": crop["crop_name"],
                "sow_month": crop["sow_month"],
                "harvest_month": crop["harvest_month"],
                "t_min": cc["t_min"],
                "t_max": cc["t_max"],
                "rain_min": cc["rain_min"],
                "rain_max": cc["rain_max"],
            })

    scored = []
    for row in rows:
        score = crop_suitability(row, climate_df)
        scored.append({
            "id": row["crop_id"],
            "name": row["crop_name"],
            "score": score
        })

    suitable = [crop for crop in scored if crop["score"] >= 0.65]
    return {"suitable_crops" : suitable}


def climate_to_dataframe(climate: Climate) -> pd.DataFrame:
    df = pd.DataFrame({
        "month": list(range(1, 13)),
        "tmin": climate.monthly_tmin,
        "tmax": climate.monthly_tmax,
        "rain": climate.monthly_rain,
        "evap": climate.monthly_evap,
        "rh": climate.monthly_rh
    })
    return df