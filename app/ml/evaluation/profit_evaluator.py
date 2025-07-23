from app.ml.core_models.climate import Climate
from app.ml.core_models.field import Field
from app.ml.core_models.crop import Crop
from app.ml.core_models.economics import Economics
from app.ml.core_models.farmer_knowledge import FarmerKnowledge

def profit_evaluation(
        crop: Crop, 
        field: Field, 
        economic: Economics, 
        climate: Climate, 
        farmer_knowledge: FarmerKnowledge,
        beneficial_rotations: list[list[str]]
) -> float:
    """
    Evaluate the profit potential of a crop based on economic data, climate and field conditions. Best 1.0 
    """
    total_field_area = field.grid.get_total_area()
    max_yield = economic.kg_yield_per_acre 
    total_yield = 0.0

    # Stress factors
    temp_factor = crop.get_temperature_stress(climate)
    rain_factor = crop.get_rain_stress(climate)
    
    for row in range(field.grid.rows):
        for col in range(len(field.grid.cell_grid[row])):
            cell = field.grid.get_cell(row, col)
            cell_yield = 0.0

            moisture_factor = crop.get_moisture_stress(cell)
            pest_factor = cell.pest_pressure

            nutrient_factor =  nutrient_penalty_factor(
                crop.n,
                cell.n,
                crop.p,
                cell.p,
                crop.k,
                cell.k
            )

            soil_factor = soil_type_penalty(crop.soil_type, cell.soil_type)
            ph_factor = ph_penalty(crop.ph_min, crop.ph_max, cell.ph)

            yield_penalty = (
                temp_factor ** 1.0 *
                rain_factor ** 1.0 *
                moisture_factor ** 1.2 *
                (1.0 - pest_factor) ** 1.3 * 
                (1.0 - nutrient_factor) ** 1.5 *
                (1.0 - ph_factor) ** 1.3 *
                (1.0 - soil_factor) ** 1.1 
            )

            cell_yield  += max_yield * (1.0 - yield_penalty)


            # Farmer knowledge boost or decrease
            prev_crop = cell.crop_history[-1] if cell.crop_history else None
            if prev_crop:
                knowledge_multiplier = farmer_knowledge_multiplier(prev_crop.name, crop.name, farmer_knowledge)
            else:
                knowledge_multiplier = 1.0

            cell_yield *= knowledge_multiplier

            # Beneficial rotations boost
            past_crops = [crop.name for crop in cell.crop_history]
            benefial_rotation_multiplier = benefial_rotations_multiplier(beneficial_rotations, crop.name, past_crops)

            cell_yield *= benefial_rotation_multiplier

            total_yield += cell_yield
            cell.yield_ = cell_yield

    
    # Calculate revenue (convert kg to tonnes)
    revenue = total_yield * economic.tonne_price_sell / 1000 
    
    # Calculate cost based on units per acre and total area
    cost = economic.unit_price * economic.units_per_acre * total_field_area

    profit = revenue - cost

    # Normalize profit to [0, 1] based on max possible profit
    max_revenue = max_yield * total_field_area * economic.tonne_price_sell / 1000 # Convert kg to tonnes
    max_possible_profit = max_revenue - cost

    if max_possible_profit > 0:
        normalized_profit = profit / max_possible_profit
    else:
        normalized_profit = 0.0
   
    normalized_profit = min(normalized_profit, 1.0)
    return normalized_profit

# ---Helper functions that are need from yield evaluation ---

def nutrient_penalty_factor(
    n_required: float, n_actual: float,
    p_required: float, p_actual: float,
    k_required: float, k_actual: float
) -> float:
    def missing(required, actual):
        if required == 0:
            return 0.0
        ratio = actual / required
        return max(0.0, 1.0 - min(ratio, 1.0))

    n_missing = missing(n_required, n_actual)
    p_missing = missing(p_required, p_actual)
    k_missing = missing(k_required, k_actual)

    total_penalty = 0.5 * n_missing + 0.25 * p_missing + 0.25 * k_missing
    return total_penalty

def soil_type_penalty(crop_soil_type: str, cell_soil_type: str) -> float:
    if crop_soil_type == cell_soil_type:
        return 0.0
    return 0.3

def ph_penalty(crop_ph_min: float, crop_ph_max: float, cell_ph: float) -> float:
    if  crop_ph_min - 0.5 <= cell_ph <= crop_ph_max + 0.5:
        return 0.0
        # Calculate how far it's outside
    if cell_ph < crop_ph_min - 0.5:
        diff = crop_ph_min - 0.5 - cell_ph
    else:
        diff = cell_ph - (crop_ph_max + 0.5)
    # Normalize (assume max penalty if diff > 1.5)
    normalized = min(diff / 1.5, 1.0)
    return normalized

def farmer_knowledge_multiplier(prev_crop: str, current_crop: str, farmer_knowledge: FarmerKnowledge) -> float:
    pair = (prev_crop, current_crop)

    effective = {(p.crop1, p.crop2): p.value for p in farmer_knowledge.effective_pairs}
    uneffective = {(p.crop1, p.crop2): p.value for p in farmer_knowledge.uneffective_pairs}

    if pair in effective:
        value = effective[pair]
        return 1.0 + 0.09 * value  
    elif pair in uneffective:
        value = uneffective[pair]
        return 1.0 - 0.09 * value  
    else:
        return 1.0
    

def benefial_rotations_multiplier(beneficial_rotations: list[list[str]], crop_name: str, past_crops: list[str]) -> float:
    rotation = [crop_name]
    for past_crop in reversed(past_crops):
        rotation.insert(0, past_crop)
        if rotation in beneficial_rotations:
            return 1.05
    
    return 1.0
    