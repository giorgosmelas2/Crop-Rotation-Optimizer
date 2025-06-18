from app.services.supabase_client import supabase

def get_required_machinery(crop_id) -> list[str]:

    machinery_results = supabase.table("crop_machinery") \
        .select("machinery_id") \
        .eq("crop_id", crop_id) \
        .execute().data
    
    machinery_ids = [entry["machinery_id"] for entry in machinery_results]

    machinery_names = supabase.table("required_machinery") \
        .select("machinery_name") \
        .in_("machinery_id", machinery_ids) \
        .execute().data
    
    required_machinery = list(machinery_name["machinery_name"] for machinery_name in machinery_names)

    return required_machinery

