from fastapi import APIRouter
from main import supabase

router = APIRouter()

@router.get("/all-crops")
async def all_crops():
    crops = supabase.table("crops") \
        .select("crop_name") \
        .execute().data
    
    crop_names = []

    for crop in crops:
        crop_names.append(crop["crop_name"])

    return crop_names