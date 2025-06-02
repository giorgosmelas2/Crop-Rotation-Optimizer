from fastapi import APIRouter
from app.models.rotation_input import RotationInfo
from app.ml.core_models.field_state import FieldState
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate
from app.models.coordinates import Coordinates
from app.ml.simulation import simulate_crop_rotation
from app.services.crop_info_service import fetch_crop_info
from app.services.climate_service import get_climate_data

router = APIRouter()

@router.post("/rotation-plan")
async def create_rotation_plan(rotation_info: RotationInfo):

    # Fetching crops' informations
    crops = fetch_crop_info(rotation_info.crops)

    # Creating a FiedlState instance from the farmer's input
    field = FieldState(
        area=rotation_info.area,
        soil_type=rotation_info.soil_type,
        fertilization=rotation_info.fertilization,
        spraying=rotation_info.spraying,
        irrigation=rotation_info.irrigation,
        n=rotation_info.n,
        p=rotation_info.p,
        k=rotation_info.k,
        ph=rotation_info.ph,
        past_crops=rotation_info.past_crops
    )

    # Creating a FarmerKnowledge instance from the farmer's input
    farmer_knowledge = FarmerKnowledge(
        effective_pairs=rotation_info.effective_pairs,
        uneffective_pairs=rotation_info.uneffective_pairs
    )

    coords = Coordinates(
        lat=rotation_info.coordinates.lat,
        lng=rotation_info.coordinates.lng
    )

    climate_df = get_climate_data(coords)

    rotation_years = rotation_info.years

    print(f"crops: {crops}")
    print(f"field: {field}")
    print(f"farmer_knowledge: {farmer_knowledge}")
    print(f"climate_df: {climate_df}")
    # simulate_crop_rotation(field, crops, farmer_knowledge, rotation_years)
    
