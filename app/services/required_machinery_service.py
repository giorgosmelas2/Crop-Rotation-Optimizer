from app.services.supabase_client import supabase
from app.ml.core_models.crop import Crop

def get_required_machinery(crops: list[Crop]) -> list[str]:

    for crop in crops:
        try:
            machinery_results = supabase.table("crop_machinery") \
                .select("machinery_id") \
                .eq("crop_id", crop.id) \
                .execute().data
            
            machinery_ids = [entry["machinery_id"] for entry in machinery_results]

            machinery_names = supabase.table("required_machinery") \
                .select("machinery_name") \
                .in_("machinery_id", machinery_ids) \
                .execute().data
            
            required_machinery = list(machinery_name["machinery_name"] for machinery_name in machinery_names)
        except Exception as e:
            print(f"Failed to fetch machinery for crop with id: {crop.id}", e)
            continue

    return required_machinery

