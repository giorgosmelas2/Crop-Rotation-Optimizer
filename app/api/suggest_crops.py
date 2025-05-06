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

    rows = []
    for c in crops:
        cc = next((cl for cl in climates if cl["crop_id"] == c["crop_id"]), None)
        if cc:
            rows.append({
                "crop_name": c["crop_name"],
                "sow_month": c["sow_month"],
                "harvest_month": c["harvest_month"],
                "t_min": cc["t_min"],
                "t_max": cc["t_max"],
                "rain_min": cc["rain_min"],
                "rain_max": cc["rain_max"],
            })

    scored = []
    for row in rows:
        score = crop_suitability(row, climate)
        scored.append((row["crop_name"], score))

    suitable = [name for name, s in scored if s >= 0.65]
    return {"suitable_crops" : suitable}