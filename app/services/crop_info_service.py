from app.services.supabase_client import supabase
from app.ml.core_models.crop import Crop
from typing import List

# Fetching the crop information from the Supabase database
def fetch_crop_info(crop_names: List[str]) -> List[Crop]:
    crops: List[Crop] = []
    for crop_name in crop_names:
        print("Fetching data for crop:", crop_name)
        try:
            crop = supabase.table("crops") \
                .select("*") \
                .eq("crop_name", crop_name) \
                .execute().data
            
            crop_cliamte = supabase.table("crop_climate") \
                .select("*") \
                .eq("crop_id", crop[0]["crop_id"]) \
                .execute().data   
            
            crop_nutrients = supabase.table("crop_nutrients") \
                .select("*") \
                .eq("crop_id", crop[0]["crop_id"]) \
                .execute().data
            
            ressidue_returns = supabase.table("residue_returns") \
                .select("*") \
                .eq("crop_id", crop[0]["crop_id"]) \
                .execute().data
            
            soil_id = supabase.table("crop_soils") \
                .select("soil_id") \
                .eq("crop_id", crop[0]["crop_id"]) \
                .execute().data
            
            soil_type = supabase.table("soils") \
                .select("soil_name") \
                .eq("soil_id", soil_id[0]["soil_id"]) \
                .execute().data
            
        except Exception as e:
            print(f"Error fetching crop data for {crop[0]["crop_id"]}: {e}")
            continue

        if crop and crop_cliamte and crop_nutrients and ressidue_returns and soil_type: 
            
            crops.append(Crop(
                crop_id = crop[0]["crop_id"],
                crop_name = crop[0]["crop_name"],
                family = crop[0]["family"],
                is_legume = crop[0]["is_legume"],
                root_depth_cm = crop[0]["root_depth_cm"],
                etc_mm = crop[0]["etc_mm"],
                sow_month = crop[0]["sow_month"],
                harvest_month = crop[0]["harvest_month"],
                t_min = crop_cliamte[0]["t_min"],
                t_max = crop_cliamte[0]["t_max"],
                t_opt_min = crop_cliamte[0]["t_opt_min"],
                t_opt_max = crop_cliamte[0]["t_opt_max"],
                rain_min_mm = crop_cliamte[0]["rain_min"],
                rain_max_mm = crop_cliamte[0]["rain_max"],
                ph_min = crop_cliamte[0]["ph_min"],
                ph_max = crop_cliamte[0]["ph_max"],
                g_min = crop_cliamte[0]["g_min"],
                g_max = crop_cliamte[0]["g_max"],
                n = crop_nutrients[0]["n"],
                p = crop_nutrients[0]["p"],
                k = crop_nutrients[0]["k"],
                soil_type = soil_type[0]["soil_name"],
                residue_fraction = ressidue_returns[0]["residue_fraction"],
                n_fix = ressidue_returns[0]["n_fix"],
                n_ret = ressidue_returns[0]["n_ret"],
                p_ret = ressidue_returns[0]["p_ret"],
                k_ret = ressidue_returns[0]["k_ret"]
            ))
            
    return crops