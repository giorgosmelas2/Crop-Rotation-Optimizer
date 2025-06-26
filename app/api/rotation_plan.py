from fastapi import APIRouter

from app.ml.core_models.field_state import FieldState
from app.ml.core_models.farmer_knowledge import FarmerKnowledge

from app.agents.pest_simulation import PestSimulationManager

from app.models.coordinates import Coordinates
from app.models.rotation_input import RotationInfo

from app.services.crop_info_service import fetch_crop_info
from app.services.climate_service import get_climate_data
from app.services.economic_service import get_economic_data
from app.services.pest_service import create_pest_agent

from app.ml.optimization.run_optimizer import optimize_rotation_plan

router = APIRouter()

@router.post("/rotation-plan")
async def create_rotation_plan(rotation_info: RotationInfo):

    # Fetching crops' informations
    crops = fetch_crop_info(rotation_info.crops)

    # Creating the pest agents of crops
    pest_agents = create_pest_agent(crops)
    pest_manager = PestSimulationManager(pest_agents)

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
        uneffective_pairs=rotation_info.uneffective_pairs,
        past_crops=rotation_info.past_crops
    )

    # Fetching climate data based on the coordinates provided
    coords = Coordinates(
        lat=rotation_info.coordinates.lat,
        lng=rotation_info.coordinates.lng
    )
    climate_df = get_climate_data(coords)

    # Fetching economic data for each crop
    economic_data = get_economic_data(crops)

    missing_machinery = rotation_info.machinery

    rotation_years = rotation_info.years

    # print(f"crops: {crops}")
    # print(f"field: {field}")
    # print(f"farmer_knowledge: {farmer_knowledge}")
    # print(f"climate_df: {climate_df}")
    # print(f"economic_data: {economic_data}")

    best_rotation, score = optimize_rotation_plan(
        crops=crops,
        pest_manager=pest_manager,
        field_state=field,
        climate_df=climate_df,
        farmer_knowledge=farmer_knowledge,
        economic_data= economic_data,
        missing_machinery=missing_machinery,
        past_crops=rotation_info.past_crops,
        years=rotation_years
    )

    print(f"Best rotation: {best_rotation}\nScore: {score}")
