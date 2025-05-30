from fastapi import APIRouter
from app.services.supabase_client import supabase

router = APIRouter()

@router.get("/crop-machinery")
async def required_machinery(id: str):
    machinery_names = []

    if id == "__all__":
        machinery = supabase.table("required_machinery") \
            .select("machinery_name") \
            .execute().data
        
        machinery_names = [item["machinery_name"] for item in machinery]
        print(machinery_names)
        return machinery_names
    
    try:
        crop_id = int(id)
    except ValueError:
        return {"error": "Invalid ID format. Must be an integer or '__all__'."}

    machinery = supabase.table("crop_machinery") \
        .select("machinery_id") \
        .eq("crop_id", crop_id) \
        .execute().data
    
    machinery_ids = [item["machinery_id"] for item in machinery]

   

    for id in machinery_ids: 
        machinery_name = supabase.table("required_machinery") \
            .select("machinery_name") \
            .eq("machinery_id", id) \
            .execute().data
        
        machinery_names.append(machinery_name[0]["machinery_name"])

    print(machinery_names)    
        
    return machinery_names



    