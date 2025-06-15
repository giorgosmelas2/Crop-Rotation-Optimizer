from app.agents.pest_agent import PestAgent
from app.ml.grid.field_grid import FieldGrid
from app.ml.grid.cell import Cell
from app.ml.core_models.crop import Crop


def update_pest_pressure(current_crop: Crop, past_crop: Crop, cell: Cell):
    """
    Updates the pest pressure in a cell based on crop rotation and spraying practices.
    
    Args:
        past_crop (Crop): The crop previously grown in the cell.
        current_crop (Crop): The crop being grown now.
        cell (Cell): The cell to update.
    """

    # Skip if any crop is missing or the past crop had no known pest
    if not past_crop or not current_crop or not past_crop.pest:
        return
    
    # Check if the same pest affects both crops
    same_pest = current_crop.pest == past_crop.pest
    same_family = past_crop.family == current_crop.family
    same_order = past_crop.order == current_crop.order

    # Base increase depends on crop relatedness
    base_increase = 0.0
    if same_family:
        base_increase = 0.25  # Same family = higher pest survival
    elif same_order:
        base_increase = 0.15   # Same order = moderate risk

    # If the pest is not shared, reduce the impact    
    if not same_pest:
        base_increase *= 0.5

    spraying_level = cell.spraying
    spraying_effect = {
        0: 1.0, # No protection
        1: 0.6,
        2: 0.3,
        3: 0.1  # High protection
    }

    spraying_factor = spraying_effect.get(spraying_level, 1.0)
    pressure_increase = base_increase * spraying_factor

    # Decay if crop is entirely unrelated to previous
    if not same_family and not same_order and not same_pest:
        decay = 0.2  # Decay from natural pest die-off or host absence
        final_pressure = cell.pest_pressure + pressure_increase - decay
    else:
        final_pressure = cell.pest_pressure + pressure_increase


    # Keep within [0, 1]
    cell.pest_pressure = max(0.0, min(final_pressure, 1.0))




