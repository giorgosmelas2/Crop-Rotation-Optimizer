import logging
from app.ml.core_models.field import Field
from app.ml.core_models.crop import Crop
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate
from app.ml.core_models.economics import Economics
from app.agents.pest_simulation import PestSimulationManager

from app.ml.simulation_logic.effects import update_soil_after_crop, update_soil_moisture_after_crop

from app.ml.evaluation.beneficial_rotations_evaluator import beneficial_rotations_evaluation
from app.ml.evaluation.climate_evaluator import climate_evaluation
from app.ml.evaluation.crop_rotation_evaluator import crop_rotation_evaluation
from app.ml.evaluation.farmer_knowledge_evaluator import farmer_knowledge_evaluation
from app.ml.evaluation.machinery_evaluator import machinery_evaluation
from app.ml.evaluation.profit_evaluator import profit_evaluation

logger = logging.getLogger("crop_rotation")
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def simulate_crop_rotation( 
        field: Field, 
        climate: Climate, 
        crops: list[Crop], 
        pest_manager: PestSimulationManager,
        farmer_knowledge: FarmerKnowledge,
        beneficial_rotations: list[list[str]],
        economic_data: dict[int, Economics],
        missing_machinery: list[str],
        crops_required_machinery: dict[int, list[str]],
        past_crops: list[str],
        years: int
    ) -> tuple[float, dict]:

    total_score = 0.0

    total_crops = len(crops)
    current_crop_index = 0

    farmer_knowledge_score = farmer_knowledge_evaluation(farmer_knowledge, crops, past_crops)
    beneficial_rotations_score = beneficial_rotations_evaluation(crops, past_crops)
    crop_rotation_score = crop_rotation_evaluation(crops)
    
    total_yield_score = 0.0
    total_climate_score = 0.0
    total_machinery_score = 0.0

    num_evaluated_crops = 0

    pest_manager.initialize_past_pest_agents(field)

    # Years + 1 if the last crop harvest month is in the next year
    for year in range(years + 1):
        logger.info(f"---Year {year + 1}---")  
        # Stop simulation if all crops have been processed
        if current_crop_index >= total_crops:
            logger.info("All crops have been sown and harvested. Stopping early.")
            break
        for month in range(1,13):
            # Current crop
            crop = crops[current_crop_index]

            # Sowing: If it's the sowing month and the field is empty, sow the crop in all cells
            if month == crop.sow_month and field.grid.is_field_empty():
                num_evaluated_crops += 1

                logger.info(f"Month {month}: sowing {crop.name} in all cells.")
                for row in range(field.grid.rows):
                    for col in range(len(field.grid.cell_grid[row])):
                        field.grid.sow_crop(row, col, crop)

                # Initialize pest for current crop
                pest_manager.initialize_pest_agents(field)

                # Evaluate climate suitability for the crop
                climate_score = climate_evaluation(climate, crop)
                total_climate_score += climate_score
                logger.debug(f"Climate score for {crop.name}: {climate_score:.2f}")
                    
                # Missing machinery evaluation
                machinery_score = machinery_evaluation(crops_required_machinery[crop.id], missing_machinery)
                total_machinery_score += machinery_score
                logger.debug(f"Machinery score for {crop.name}: {machinery_score}")
            # Harvesting: If it's the harvest month and the field is not empty, harvest the crop in all cells
            elif month == crop.harvest_month and not field.grid.is_field_empty():
                # Evaluate total profit
                profit_score = profit_evaluation(crop, field, economic_data.get(crop.id), climate, farmer_knowledge, beneficial_rotations)
                total_profit_score += profit_score
                logger.debug(f"Yield score for {crop.name}: {profit_score:.2f}")

                logger.info(f"Month {month}: harvesting {crop.name} in all cells.")
                for row in range(field.grid.rows):
                    for col in range(len(field.grid.cell_grid[row])):
                        cell = field.grid.get_cell(row, col)
                        update_soil_moisture_after_crop(crop, cell, climate)
                        update_soil_after_crop(crop, cell) 
                        field.grid.harvest_crop(row, col)

                current_crop_index += 1
                # If all crops have been processed, stop the simulation
                if current_crop_index >= total_crops : 
                    logger.info("All crops have been sown and harvested.")
                    break
            
            pest_manager.step(field)

    final_profit_score = total_profit_score / num_evaluated_crops
    final_climate_score = total_climate_score / num_evaluated_crops
    final_machinery_score = total_machinery_score / num_evaluated_crops

    logger.debug(f"final_profit_score: {final_profit_score}")
    logger.debug(f"final_climate_score: {final_climate_score}")
    logger.debug(f"final_machinery_score: {final_machinery_score}")
    logger.debug(f"farmer_knowledge_score: {farmer_knowledge_score}")
    logger.debug(f"beneficial_rotations_score: {beneficial_rotations_score}")
    logger.debug(f"crop_rotation_score: {crop_rotation_score}")

    total_score = (
        0.4 * final_profit_score +
        0.19 * farmer_knowledge_score + 
        0.12 * beneficial_rotations_score + 
        0.11 * final_climate_score +
        0.1 * crop_rotation_score + 
        0.08 * final_machinery_score
    )

    logger.debug(f"Total score: {total_score}")
    return total_score
   
    
    
    
       


