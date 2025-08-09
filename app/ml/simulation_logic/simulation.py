import logging
from app.ml.core_models.field import Field
from app.ml.core_models.crop import Crop
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate
from app.ml.core_models.economics import Economics
from app.agents.pest_simulation import PestSimulationManager

from app.ml.evaluation.beneficial_rotations_evaluator import beneficial_rotations_evaluation
from app.ml.evaluation.climate_evaluator import climate_evaluation
from app.ml.evaluation.crop_rotation_evaluator import crop_rotation_evaluation
from app.ml.evaluation.farmer_knowledge_evaluator import farmer_knowledge_evaluation
from app.ml.evaluation.machinery_evaluator import machinery_evaluation
from app.ml.evaluation.profit_evaluator import profit_evaluation

BASE_ROTATION_WEIGHTS = {
"profit": 0.4,
"farmer_knowledge": 0.19,
"beneficial_rotations": 0.12,
"climate": 0.11,
"crop_rotation": 0.1,
"machinery": 0.08,
}

def simulate_crop_rotation( 
        selected_crops: list[Crop],
        field: Field, 
        climate: Climate, 
        crops_ids: list[int], 
        pest_manager: PestSimulationManager,
        farmer_knowledge: FarmerKnowledge,
        beneficial_rotations: list[list[str]],
        economic_data: dict[int, Economics],
        missing_machinery: list[str],
        crops_required_machinery: dict[int, list[str]],
        past_crops: list[str],
        years: int
    ) -> float:

    """
    Simulates a multi-year crop rotation and evaluates its overall performance.

    This function performs month-by-month simulation of crop growth,
    pest pressure, soil and moisture dynamics, and evaluates each crop
    for profitability, climate suitability, machinery availability, and rotation benefits.

    For each crop:
      - Sowing and harvesting are simulated in the correct months.
      - Pests are initialized and spread over time.
      - Soil nutrients and moisture are updated after harvesting.
      - Multiple evaluation scores are computed per crop.

    Final score is a weighted combination of:
      - Profitability (40%)
      - Farmer knowledge effectiveness (19%)
      - Beneficial rotation sequences (12%)
      - Climate suitability (11%)
      - Crop rotation health (root depth & legumes) (10%)
      - Machinery availability (8%)

    Returns:
        total_score (float): Final normalized score of the rotation (0.0-1.0).
    """
    id_to_crop = {crop.id: crop for crop in selected_crops}
    crops =  get_crops_from_ids(crops_ids, id_to_crop)

    total_score = 0.0

    total_crops = len(crops)
    current_crop_index = 0

    crop_names = [crop.name for crop in crops]
    farmer_knowledge_score = farmer_knowledge_evaluation(farmer_knowledge, crop_names.copy(), past_crops)
    beneficial_rotations_score = beneficial_rotations_evaluation(crop_names.copy(), past_crops, beneficial_rotations)
    crop_rotation_score = crop_rotation_evaluation(crops)
    
    total_profit_score = 0.0
    total_climate_score = 0.0
    total_machinery_score = 0.0

    num_evaluated_crops = 0

    if past_crops:
        pest_manager.initialize_past_pest_agents(field)

    climate_score_cache: dict[int, float] = {}
    machinery_score_cache: dict[int, float] = {}

    simulation_step_counter = 0

    # Years + 1 if the last crop harvest month is in the next year
    for year in range(years + 1):

        # Stop simulation if all crops have been processed
        if current_crop_index >= total_crops:
            break

        sow_month = crops[current_crop_index].sow_month
        harvest_month = crops[current_crop_index].harvest_month

        for month in range(1,13):
            # Current crop
            crop = crops[current_crop_index]

            # Sowing: If it's the sowing month and the field is empty, sow the crop in all cells
            if month == sow_month and field.grid.is_field_empty():
                num_evaluated_crops += 1

                # Sowing the crop in all cells
                field.grid.sow_crop_to_all(crop)

                # Initialize pest for current crop
                pest_manager.initialize_pest_agents(field)

                # Evaluate climate suitability for the crop
                if crop.id in climate_score_cache:
                    climate_score = climate_score_cache[crop.id]
                else:
                    climate_score = climate_evaluation(climate, crop)
                    climate_score_cache[crop.id] = climate_score
                total_climate_score += climate_score
                    
                # Missing machinery evaluation
                if crop.id in machinery_score_cache:
                    machinery_score = machinery_score_cache[crop.id]
                else:
                    machinery_score = machinery_evaluation(crops_required_machinery[crop.id], missing_machinery)
                    machinery_score_cache[crop.id] = machinery_score
                total_machinery_score += machinery_score

            # Harvesting: If it's the harvest month and the field is not empty, harvest the crop in all cells
            elif month == harvest_month and not field.grid.is_field_empty():
                # Evaluate total profit
                profit_score = profit_evaluation(crop, field, economic_data.get(crop.id), climate, farmer_knowledge, beneficial_rotations)
                total_profit_score += profit_score

                # Harvesting the crop in all cells
                field.grid.harvest_all(crop, climate)

                current_crop_index += 1
                # If all crops have been processed, stop the simulation
                if current_crop_index >= total_crops : 
                    break

            if simulation_step_counter % 2 == 0:
                pest_manager.step(field)
            simulation_step_counter += 1

    if num_evaluated_crops == 0:
        return 0.0

    final_profit_score = total_profit_score / num_evaluated_crops
    final_climate_score = total_climate_score / num_evaluated_crops
    final_machinery_score = total_machinery_score / num_evaluated_crops
    
    score_components = {
        "profit": final_profit_score,
        "farmer_knowledge": farmer_knowledge_score,
        "beneficial_rotations": beneficial_rotations_score,
        "climate": final_climate_score,
        "crop_rotation": crop_rotation_score,
        "machinery": final_machinery_score,
    }   
    # If thre is no farmer knowledge the wheight has to be 0 and other weights will be adjuste
    has_farmer_knowledge = bool(farmer_knowledge.effective_pairs or farmer_knowledge.uneffective_pairs)
    weights = BASE_ROTATION_WEIGHTS.copy()
    if not has_farmer_knowledge:
        weights["farmer_knowledge"] = 0.0

    total_active_weight = sum(weights.values())
    if total_active_weight == 0:
        total_score = 0.0
    else:
        normalized_weights = {k: w / total_active_weight for k, w in weights.items()}
        total_score = sum(score_components[k] * normalized_weights[k] for k in score_components)

    return total_score
   
    
# Helper function that returns the Crop objectives from ids
def get_crops_from_ids(crop_ids: list[int], id_to_crop: dict[int, Crop]) -> list[Crop]:
    crops = []
    for cid in crop_ids:
        crop = id_to_crop.get(cid)
        if crop is None:
            raise ValueError(f"Crop id {cid} not found among selected_crops")
        crops.append(crop)
    return crops


