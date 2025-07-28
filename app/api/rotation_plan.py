from fastapi import APIRouter
from app.services.supabase_client import supabase

from app.ml.core_models.field import Field
from app.ml.core_models.farmer_knowledge import FarmerKnowledge

from app.agents.pest_simulation import PestSimulationManager

from app.models.coordinates import Coordinates
from app.models.rotation_input import RotationInfo

from app.ml.grid.field_grid import FieldGrid
from app.ml.grid.grid_utils import cell_create

from app.services.crop_info_service import fetch_crop_info
from app.services.climate_service import get_climate_data
from app.services.economic_service import get_economic_data
from app.services.pest_service import create_pest_agent
from app.services.required_machinery_service import get_required_machinery
from app.services.beneficial_rotations_service import get_beneficial_rotations

from app.ml.optimization.run_optimizer import optimize_rotation_plan

from visualization.plots import all_plots
router = APIRouter()

@router.post("/rotation-plan")
async def create_rotation_plan(rotation_info: RotationInfo):

    # Fetching crops' informations
    crops = fetch_crop_info(rotation_info.crops)
    past_crops = fetch_crop_info(rotation_info.past_crops)

    past_crops_names = [crop.name for crop in past_crops]
    past_pest_agents = create_pest_agent(past_crops_names)

    # Creating the pest agents of crops
    crop_names = [crop.name for crop in crops]
    pest_agents = create_pest_agent(crop_names)
    pest_manager = PestSimulationManager(pest_agents, past_pest_agents)

    # Creating field based on the rotation information
    cells = cell_create(rotation_info)
    field_grid = FieldGrid(cells=cells)
    field = Field(
        total_area=rotation_info.area,
        grid=field_grid
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
    climate = get_climate_data(coords)

    # Fetching economic data for each crop
    economic_data = get_economic_data(crops)

    crops_required_machinery = get_required_machinery(crops)
    beneficial_rotations = get_beneficial_rotations()

    missing_machinery = rotation_info.machinery

    rotation_years = rotation_info.years

    best_individual, best_score, gens_best_fitness, gens_avg_fitness, gens_variance, gens_worst_fitness = optimize_rotation_plan(
        crops=crops,
        pest_manager=pest_manager,
        field=field,
        climate=climate,
        farmer_knowledge=farmer_knowledge,
        beneficial_rotations=beneficial_rotations,
        economic_data= economic_data,
        missing_machinery=missing_machinery,
        crops_required_machinery=crops_required_machinery,
        past_crops=past_crops,
        years=rotation_years
    )

    print(f"Best rotation: {best_individual}\nBest score: {best_score}\n")
    # all_plots(
    #     gens_best_fitness=gens_best_fitness,
    #     gens_avg_fitness=gens_avg_fitness,
    #     gens_variance=gens_variance,
    #     gens_worst_fitness=gens_worst_fitness,
    # )

    user_id = rotation_info.user_id

    data = {
        "user_id": user_id,
        "years": rotation_info.years,
        "crops": best_individual  
    }

    result = supabase.table("crop_plans").insert(data).execute()

    print("Inserted to Supabase:", result)