from app.services.supabase_client import supabase

def get_beneficial_rotations() -> list[list[str]]:
    data = supabase.table("beneficial_rotations") \
        .select("*") \
        .execute().data
    
    rotations_ids: list[list[int]] = []
    
    for rec in data:
        row = [
            rec["first_crop_id"],
            rec["second_crop_id"]
        ]

        for key in ("third_crop_id", "forth_crop_id", "fifth_crop_id"):
            if rec.get(key) is not None:
                row.append(rec[key])
        rotations_ids.append(row)

    all_ids = {crop_id for row in rotations_ids for crop_id in row}
    crop_records = supabase.table("crops") \
        .select("crop_id, crop_name") \
        .in_("crop_id", list(all_ids)) \
        .execute().data
    
    id_to_name = {r["crop_id"]: r["crop_name"] for r in crop_records}

    rotations_names: list[list[str]] = []
    
    for row in rotations_ids:
        names_row: list[str] = []

        for id in row:
            name = id_to_name.get(id)
            if name: 
                names_row.append(name)
        
        rotations_names.append(names_row)

    return rotations_names




