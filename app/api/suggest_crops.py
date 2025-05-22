from pydantic import BaseModel
from fastapi import APIRouter
from app.services.climate_service import get_climatology
from app.services.suitability_service import crop_suitability
from main import supabase

router = APIRouter()

class Location(BaseModel):
    lat: float
    lon: float

@router.post("/suggest-crops")
async def suggest(req: Location):
    climate = get_climatology(req.lat, req.lon)

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
        score = crop_suitability(row, climate)
        scored.append({
            "id": row["crop_id"],
            "name": row["crop_name"],
            "score": score
        })

    suitable = [crop for crop in scored if crop["score"] >= 0.65]
    return {"suitable_crops" : suitable}