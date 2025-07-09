import pandas as pd
from app.ml.core_models.crop import Crop
from app.ml.core_models.economics import Economics
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate

from app.ml.core_models.field import Field

from app.services.beneficial_rotations_service import get_beneficial_rotations

def climate_evaluation(climate: Climate, crop: Crop) -> float:
    """
    Evaluate the suitability of the climate for a given crop based on temperature and rainfall.
    Args:
        climate_df (dict): DataFrame containing climate data with columns 'month', 'tmin', 'tmax', and 'rain'.
        crop (Crop): The crop to evaluate.
    Returns:
        float: A score representing the suitability of the climate for the crop.
    """
    # Constants
    TOL = 4  # Tolerance for temperature

    total_temperature_score = 0.0
    rain_score = 0.0

    sow = crop.sow_month
    harvest = crop.harvest_month

    # --- Temperature Evaluation ---
    active_tmin = climate.get_tmin(sow, harvest)
    active_tmax = climate.get_tmax(sow, harvest)

    # Calculating temperature score
    t_min_deviation = (crop.t_min - active_tmin["tmin"]).clip(lower=0)
    t_max_deviation = (active_tmax["tmax"] - crop.t_max).clip(lower=0)

    # 1 if temperature is ok, <1 if is a little more, 0 if is not ok
    t_min_score = (1 - (t_min_deviation / TOL)).clip(lower=0)
    t_max_score = (1 - (t_max_deviation / TOL)).clip(lower=0)

    # Calculating optimal temperature score
    t_opt_min_deviation = (crop.t_opt_min - active_tmin).clip(lower=0)
    t_opt_max_deviation = (active_tmax - crop.t_opt_max).clip(lower=0)

    # 1 if temperature is ok, <1 if is a little more, 0 if is not ok
    t_opt_min_score = (1 - (t_opt_min_deviation / TOL)).clip(lower=0)
    t_opt_max_score = (1 - (t_opt_max_deviation / TOL)).clip(lower=0)

    temp_score = (t_min_score + t_max_score) / 2
    temperature_score = temp_score.mean() * 0.3 # Average of all months

    temp_opt_score = (t_opt_min_score + t_opt_max_score) / 2
    temperature_opt_score = temp_opt_score.mean() * 0.7  # Average of all months

    total_temperature_score = temperature_score + temperature_opt_score

    # --- Rain Evaluation ---
    total_rain = climate.get_rain(sow, harvest)

    RAIN_TOLERANCE = 0.1
    RAIN_PENALTY_FACTOR = 1.5

    if crop.rain_min_mm <= total_rain <= crop.rain_max_mm:
        rain_score = 1.0
    else:
        if total_rain < crop.rain_min_mm:
            diff_percent = (crop.rain_min_mm - total_rain) / crop.rain_min_mm
        else: 
            diff_percent = (total_rain - crop.rain_max_mm) / crop.rain_max_mm
        
        if diff_percent <= RAIN_TOLERANCE:
            rain_score = 1.0
        else:
            rain_score = max(0.0, 1.0 - (diff_percent - RAIN_TOLERANCE) * RAIN_PENALTY_FACTOR)

    # Final score
    final_score = (total_temperature_score + rain_score) / 2  
    return final_score


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

def farmer_knowledge_evaluation(farmer_knowledge: FarmerKnowledge, crops: list[Crop], past_crops: list[str]) -> float:
    """
    Evaluate the farmer's knowledge based on the crop's requirements and the farmer's knowledge.
    Args:
        farmer_knowledge (FarmerKnowledge): FarmerKnowledge data containing effective and uneffective crop pairs that farmer has observed
        crop_list (List[Crop]): List of crops to evaluate.
    Returns:
        float: A score representing the farmer's knowledge for the crop.
    """
    last_crop = past_crops[-1]
    crop_names = [last_crop] + [crop.name for crop in crops]

    crop_pairs = list(zip(crop_names, crop_names[1:]))
    effective_pairs = {
        (pair.crop1, pair.crop2): pair.value
        for pair in farmer_knowledge.effective_pairs

    }
    uneffectibe_pairs = {
        (pair.crop1, pair.crop2): pair.value
        for pair in farmer_knowledge.uneffective_pairs
    }

    score = 0 
    for pair in crop_pairs: 
        if pair in effective_pairs:
            score += effective_pairs[pair]
        elif pair in uneffectibe_pairs:
            score += uneffectibe_pairs[pair]

    max_score_possible = len(crop_pairs) * 3  
    normalized_score = (score + max_score_possible) / (2 * max_score_possible)

    return normalized_score


def machinery_evaluation(required_machinery: list[str], missing_machinery: list[str]) -> float:
    for machinery in required_machinery:
        if machinery in missing_machinery:
            return 0.0
        
    return 1.0

def crop_rotation_evaluation(crops: list[Crop]) -> float:
    root_score = 0.0

    #--- Root depth alternation ---
    alternation_count = 0
    for prev, curr in zip(crops, crops[1:]):
        if abs(prev.root_depth_cm - curr.root_depth_cm) >= 30:
            alternation_count += 1
    
    root_score = alternation_count / (len(crops) - 1)

    #--- Legume bonus ---
    non_legume_streak = 0
    violations = 0
    for crop in crops:
        if crop.is_legume:
            non_legume_streak = 0
        else:
            non_legume_streak += 1
            if non_legume_streak >= 3:
                violations += 1
                non_legume_streak = 0

    
    max_violations = len(crops) // 3 or 1
    legume_score = max(0.0, 1.0 - (violations / max_violations))   
        
    
    final_score = 0.3 * root_score + 0.7 * legume_score
    return final_score

def beneficial_rotations_evaluation(crops: list[Crop], past_crops: list[str]) -> float:
    beneficial_rotations = get_beneficial_rotations()
    last_crop = past_crops[-1] # Only the last crop
    crop_names = [last_crop] + [crop.name for crop in crops]
    total_benefial_sequences = 0
    total_windows = 0

    for rotation in beneficial_rotations:
        rot_len = len(rotation)
        max_start = len(crop_names) - rot_len + 1
        total_windows += max(0, max_start)
        for i in range(max_start):
            if crop_names[i:i + rot_len] == rotation:
                total_benefial_sequences += 1

    if total_windows == 0:
        return 0.0

    return total_benefial_sequences / total_windows


#--- Helper functions that are need from evaluation functions---

def nutrient_factor(required, actual):
    if actual >= required:
        return 1.0
    return actual / required

