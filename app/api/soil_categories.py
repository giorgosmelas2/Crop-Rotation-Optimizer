from fastapi import APIRouter
from app.services.supabase_client import supabase

router = APIRouter()

@router.get("/soil-categories")
async def soil_info():
    soils = supabase.table("soils") \
    .select("soil_name") \
    .execute().data

    soil_categories = []
    for soil in soils:
        soil_categories.append(soil["soil_name"]) 

    return soil_categories