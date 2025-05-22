from fastapi import APIRouter
from main import supabase

router = APIRouter()

@router.get("/all-crops")
async def all_crops():
    crops = supabase.table("crops") \
        .select("crop_id, crop_name") \
        .execute().data
    
    crop_data = {}

    for crop in crops:
        key = crop["crop_id"]
        value = crop["crop_name"]
        crop_data[key] = value
        

    return crop_data