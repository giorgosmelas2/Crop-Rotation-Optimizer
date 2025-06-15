from app.agents.pest_agent import PestAgent
from app.services.supabase_client import supabase

def create_pest_agent(crop_names: list[str]) -> list[PestAgent]:
    pest_agents = []
    for crop_name in crop_names: 
        try:
            crop = supabase.table("crops") \
                .select("crop_id, family, order") \
                .eq("crop_name", crop_name) \
                .execute().data
            
            crop_id = crop[0]["crop_id"]

            pest_id_result = supabase.table("crop_pests") \
                .select("pest_id") \
                .eq("crop_id", crop_id) \
                .execute().data
            
            pest_id = pest_id_result[0]["pest_id"]
            
            pest_name_result = supabase.table("pests") \
                .select("pest_name") \
                .eq("pest_id", pest_id) \
                .execute().data
            
            pest_name = pest_name_result[0]["pest_name"]
            
            crop_ids_result = supabase.table("crop_pests") \
                .select("crop_id") \
                .eq("pest_id", pest_id) \
                .execute().data
            
            crop_ids_list = [entry["crop_id"] for entry in crop_ids_result]

            related_crops = supabase.table("crops") \
                .select("crop_name, family") \
                .in_("crop_id", crop_ids_list) \
                .execute().data

            affected_crops = list({crop["crop_name"] for crop in related_crops})
            affected_families = list({crop["family"] for crop in related_crops})

            pest_agent = PestAgent(
                name=pest_name,
                affected_crops=affected_crops,
                affected_families=affected_families
            )

            pest_agents.append(pest_agent)


        except Exception as e:
            print(f"Problem fetching pest info for crop: {crop_name}", e)
            return None
        
    return pest_agents
        


    
    