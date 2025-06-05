from copy import deepcopy
from typing import List, Dict

from app.ml.core_models.field_state import FieldState
from app.ml.core_models.crop import Crop
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate

from app.ml.grid.field_grid import FieldGrid
from app.ml.grid.grid_utils import cell_create

from app.ml.simulation_logic.soil_dynamics import update_soil_after_crop


def simulate_crop_rotation( field_state: FieldState, climate: Climate, crops: List[Crop], farmer_knowledge: FarmerKnowledge, years: int) -> Dict:
    # Create a deep copy of the field state to avoid modifying the original
    field = deepcopy(field_state)

    # Create a grid of cells based on the field state to represent the field
    cells = cell_create(field.area, field)

    # Create a FieldGrid instance with the created cells
    field_grid = FieldGrid(cells=cells)

    total_crops = len(crops)
    current_crop_index = 0

    for year in range(years):
        print(f"---Year {year + 1}---")
        if current_crop_index >= total_crops:
            print("All crops have been sown and harvested. Stopping early.")
            break
        for month in range(1,13):
            print(f"Month {month}:")
            if month == crops[current_crop_index].sow_month and field_grid.is_field_empty():
                print(f"Sowing {crops[current_crop_index].name} in all cells.")

                # Sow the current crop in all cells of the field grid
                for row in range(field_grid.rows):
                    for col in range(len(field_grid.grid[row])):
                        field_grid.sow_crop(row, col, crops[current_crop_index].name)

            elif month == crops[current_crop_index].harvest_month and not field_grid.is_field_empty():
                print(f"Harvesting {crops[current_crop_index].name} in all cells.")

                # Harvest the current crop in all cells of the field grid
                for row in range(field_grid.rows):
                    for col in range(len(field_grid.grid[row])):
                        field_grid.harvest_crop(row, col)
                        cell = field_grid.get_cell(row, col)
                        update_soil_after_crop(crops[current_crop_index], cell)  

                current_crop_index += 1
                if current_crop_index >= total_crops :
                    print("All crops have been sown and harvested.")
                    break

        print("Updated cell states:")
        field_grid.print_nutrients()
   
    
    
    
       


