from copy import deepcopy
from typing import Dict

from app.ml.core_models.field_state import FieldState
from app.ml.core_models.crop import Crop
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate
from app.ml.core_models.economics import Economics

from app.ml.grid.field_grid import FieldGrid
from app.ml.grid.grid_utils import cell_create

from app.ml.simulation_logic.effects import update_soil_after_crop
from app.ml.simulation_logic.evaluation import climate_evaluation, profit_evaluation, farmer_knowledge_evaluation, machinery_evaluation, crop_rotation_evaluation

from app.agents.pest_simulation import PestSimulationManager

from app.services.pest_service import create_pest_agent
from app.services.required_machinery_service import get_required_machinery

def simulate_crop_rotation( 
        field_state: FieldState, 
        climate_df: Climate, 
        crops: list[Crop], 
        farmer_knowledge: FarmerKnowledge, 
        economic_data: list[Economics],
        missing_machinery: list[str],
        years: int
    ) -> Dict:

    # Create a deep copy of the field state to avoid modifying the original
    field = deepcopy(field_state)

    # Create a grid of cells based on the field state to represent the field
    cells = cell_create(field.area, field)

    # Initialize the FieldGrid with the created cells
    field_grid = FieldGrid(cells=cells)

    pest_agents = create_pest_agent([crop.name for crop in crops])
    pest_manager = PestSimulationManager(pest_agents)

    total_score = 0.0

    total_crops = len(crops)
    current_crop_index = 0

    farmer_knowledge_score = farmer_knowledge_evaluation(farmer_knowledge, crops)
    crop_rotation_score = crop_rotation_evaluation(crops)
    
    crops_required_machinery = get_required_machinery([crop.id for crop in crops])

    for year in range(years):
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
            if month == crop.sow_month and field_grid.is_field_empty():
                print(f"Sowing {crop.name} in all cells.")
                for row in range(field_grid.rows):
                    for col in range(len(field_grid.grid[row])):
                        field_grid.sow_crop(row, col, crop.name)

                # Evaluate climate suitability for the crop
                climate_score = climate_evaluation(climate_df, crop)
                print(f"Climate suitability score for {crop.name}: {climate_score:.2f}")
                    
                # Missing machinery evaluation
                machinery_score = machinery_evaluation(crops_required_machinery[current_crop_index], missing_machinery)
            
            if not field_grid.is_field_empty():
                pest_manager.step(field_grid)

            # Harvesting: If it's the harvest month and the field is not empty, harvest the crop in all cells

            elif month == crop.harvest_month and not field_grid.is_field_empty():
                # Evaluate total profit
                yield_score = profit_evaluation(economic_data[current_crop_index], crop, field_grid, climate_df)
                print(f"Profit potential score for {crop.name}: {yield_score:.2f}")


                print(f"Harvesting {crops[current_crop_index].name} in all cells.")
                for row in range(field_grid.rows):
                    for col in range(len(field_grid.grid[row])):
                        field_grid.harvest_crop(row, col)
                        cell = field_grid.get_cell(row, col)
                        update_soil_after_crop(crops[current_crop_index], cell)  

                current_crop_index += 1
                # If all crops have been processed, stop the simulation
                if current_crop_index >= total_crops :
                    print("All crops have been sown and harvested.")
                    break
    total_score = (
        0.45 * yield_score +
        0.25 * farmer_knowledge_score + 
        0.12 * farmer_knowledge_score + 
        0.1 * crop_rotation_score + 
        0.08 * machinery_score
    )

    print("Total score: ", total_score)
   
    
    
    
       


