from copy import deepcopy
import json
import os

from app.ml.core_models.field import Field
from app.ml.core_models.crop import Crop
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate
from app.ml.core_models.economics import Economics

from app.ml.simulation_logic.effects import update_soil_after_crop
from app.ml.simulation_logic.evaluation import climate_evaluation, profit_evaluation, farmer_knowledge_evaluation, machinery_evaluation, crop_rotation_evaluation, beneficial_rotations_evaluation

from app.agents.pest_simulation import PestSimulationManager
from app.agents.pest_agent import PestAgent

def simulate_crop_rotation( 
        field: Field, 
        climate: Climate, 
        crops: list[Crop], 
        pest_manager: PestSimulationManager,
        farmer_knowledge: FarmerKnowledge, 
        economic_data: list[Economics],
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
    pest_tracking = {}

    # Years + 1 if the last crop harvest month is in the next year
    for year in range(years + 1):
        print(f"---Year {year + 1}---")  
        # Stop simulation if all crops have been processed
        if current_crop_index >= total_crops:
            print("All crops have been sown and harvested. Stopping early.")
            break
        for month in range(1,13):
            print(f"Month {month}:")

            # Current crop
            crop = crops[current_crop_index]

            # Sowing: If it's the sowing month and the field is empty, sow the crop in all cells
            if month == crop.sow_month and field.grid.is_field_empty():
                num_evaluated_crops += 1

                print(f"Sowing {crop.name} in all cells.")
                for row in range(field.grid.rows):
                    for col in range(len(field.grid.cell_grid[row])):
                        field.grid.sow_crop(row, col, crop)

                # Evaluate climate suitability for the crop
                climate_score = climate_evaluation(climate, crop)
                total_climate_score += climate_score
                print(f"Climate suitability score for {crop.name}: {climate_score:.2f}")
                    
                # Missing machinery evaluation
                machinery_score = machinery_evaluation(crops_required_machinery[crop.id], missing_machinery)
                total_machinery_score += machinery_score
            # Harvesting: If it's the harvest month and the field is not empty, harvest the crop in all cells
            elif month == crop.harvest_month and not field.grid.is_field_empty():
                # Evaluate total profit
                yield_score = profit_evaluation(economic_data[crop.id], crop, field, climate)
                total_yield_score += yield_score
                print(f"Profit potential score for {crop.name}: {yield_score:.2f}")

                print(f"Harvesting {crops[current_crop_index].name} in all cells.")
                for row in range(field.grid.rows):
                    for col in range(len(field.grid.cell_grid[row])):
                        cell = field.grid.get_cell(row, col)
                        field.grid.harvest_crop(row, col)
                        update_soil_after_crop(crops[current_crop_index], cell)  

                current_crop_index += 1
                # If all crops have been processed, stop the simulation
                if current_crop_index >= total_crops : 
                    print("All crops have been sown and harvested.")
                    break
            
            if not field.grid.is_field_empty():
                print("Step function called for pest manager.")
                pest_manager.step(field)

            for row in range(field.grid.rows):
                for col in range(len(field.grid.cell_grid[row])):
                    month_key = f"{year + 1}-{month}"
                    cell = field.grid.get_cell(row, col)
                    if (row, col) not in pest_tracking:
                        pest_tracking[(row, col)] = {}
                    pest_tracking[(row, col)][month_key] = cell.pest_pressure


    final_yield_score = total_yield_score / num_evaluated_crops
    final_climate_score = total_climate_score / num_evaluated_crops
    final_machinery_score = total_machinery_score / num_evaluated_crops
    
    total_score = (
        0.4 * final_yield_score +
        0.19 * farmer_knowledge_score + 
        0.12 * beneficial_rotations_score + 
        0.11 * final_climate_score +
        0.1 * crop_rotation_score + 
        0.08 * final_machinery_score
    )

    print("Total score: ", total_score)

    return total_score, pest_tracking
   
    
    
    
       


