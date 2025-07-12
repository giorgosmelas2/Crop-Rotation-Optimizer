import pandas as pd
from app.ml.core_models.crop import Crop
from app.ml.core_models.economics import Economics
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate

from app.ml.core_models.field import Field

from app.services.beneficial_rotations_service import get_beneficial_rotations

def profit_evaluation(economic_data: Economics, crop: Crop, field: Field, climate_df: pd.DataFrame) -> float:
    """
    Evaluate the profit potential of a crop based on economic data and field conditions.
    Args:
        economic_data (Economics): Economic data for the crop.
        crop (Crop): The crop to evaluate.
        field (FieldGrid): The field grid representing the field.
        climate_df (pd.DataFrame): DataFrame containing climate data with columns 'month', 'tmin', 'tmax', and 'rain'.
    Returns:
        float: A score representing the profit potential of the crop.
    """
    # Multipliers for each practice level (0: none, 1: partial, 2: good, 3: full)
    practice_multipliers = {
        0: 0.5,
        1: 0.7,   
        2: 0.85,  
        3: 1.0    
    }
    
    total_field_area = field.grid.get_total_area()
    max_yield = economic_data.kg_yield_per_acre 
    total_yield = 0.0
    
    # Calculate the climate suitability factor for this crop
    climate_factor = climate_evaluation(climate_df, crop)

    for row in range(field.grid.rows):
        for col in range(len(field.grid.grid[row])):
            cell = field.grid.get_cell(row, col)

            # Calculate the effect of irrigation, fertilization, and spraying
            practice_factor = (
                practice_multipliers.get(cell.irrigation, 0.5) *
                practice_multipliers.get(cell.fertilization, 0.5) *
                practice_multipliers.get(cell.spraying, 0.5)
            )

            # Calculate the effect of nutrients (N, P, K)
            nutrient_factor_total = (
                nutrient_factor(crop.n, cell.n) *
                nutrient_factor(crop.p, cell.p) *
                nutrient_factor(crop.k, cell.k)
            )

            # Combine all factors to get the actual yield for this cell
            actual_yield = max_yield * practice_factor * nutrient_factor_total * climate_factor

            # Reduce yield if soil type does not match
            if crop.soil_type != cell.soil_type:
                actual_yield *= 0.85 

            # Reduce yield if pH is out of tolerance range
            ph_tolerance = 0.5 
            if cell.ph < crop.ph_min - ph_tolerance or cell.ph > crop.ph_max + ph_tolerance:
                actual_yield *= 0.8
            
            # Reduce yield based on pest pressure (0 = no pests, 1 = total loss)
            pest_factor = max(0.0, 1.0 - cell.pest_pressure)
            actual_yield *= pest_factor

            total_yield += actual_yield
            cell.yield_ = actual_yield
    
    # Calculate revenue (convert kg to tonnes)
    revenue = total_yield * economic_data.tonne_price_sell / 1000 
    
    # Calculate cost based on units per acre and total area
    cost = economic_data.unit_price * economic_data.units_per_acre * total_field_area

    profit = revenue - cost

    # Normalize profit to [0, 1] based on max possible profit
    max_revenue = max_yield * total_field_area * economic_data.tonne_price_sell / 1000 # Convert kg to tonnes
    max_possible_profit = max_revenue - cost

    if max_possible_profit > 0:
        normalized_profit = profit / max_possible_profit
    else:
        normalized_profit = 0.0
   
    return normalized_profit



#--- Helper functions that are need from evaluation functions---

def nutrient_factor(required, actual):
    if actual >= required:
        return 1.0
    return actual / required

