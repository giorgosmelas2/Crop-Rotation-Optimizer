from typing import List

from app.services.supabase_client import supabase
from app.ml.core_models.crop import Crop
from app.ml.core_models.economics import Economics


def get_economic_data(crops: List[Crop]) -> List[Economics]: 

    economy_list = []

    for crop in crops:
        try:
            result = supabase.table("crop_economics") \
                .select("*") \
                .eq("crop_id", crop.id) \
                .execute().data
        except Exception as e:
            print(f"Error fetching economic data for crop {crop.id}: {e}")
            return None
        
        if result:
            economy_list.append(
                Economics(
                    crop_id=result[0]["crop_id"],
                    tonne_price_sell=result[0]["tonne_price_sell"],
                    unit_price=result[0]["unit_price"],
                    units_per_acre=result[0]["units_per_acre"],
                    kg_yield_per_acre=result[0]["kg_yield_per_acre"]
                )
            )
        
    return economy_list
