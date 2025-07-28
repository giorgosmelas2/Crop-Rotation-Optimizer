from fastapi import APIRouter, Query
from app.services.supabase_client import supabase

router = APIRouter()

@router.get("/user-crop-plans")
def get_user_crop_rotations(user_id: str = Query(...)):
    try:
        response = supabase.table("crop_plans") \
        .select("years, crops, created_at") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .execute().data
     
        return {"rotations": response}

    except Exception as e:
        return {"error": str(e)}