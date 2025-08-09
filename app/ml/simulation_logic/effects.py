from app.ml.grid.cell import Cell
from app.ml.core_models.crop import Crop
from app.ml.core_models.climate import Climate

def update_soil_after_crop(crop: Crop, cell: Cell): 
    """
    Update the soil nutrients in a cell after a crop is harvested.
    """
    # To decrease the run time of GA
    fertilization = cell.fertilization
    cell_n = cell.n
    cell_p = cell.p
    cell_k = cell.k

    crop_n = crop.n
    crop_p = crop.p
    crop_k = crop.k

    residue_fraction = crop.residue_fraction


    # Nutrient subtractions based on the crop's nutrient uptake
    n_subtracted = cell_n - crop_n
    p_subtracted = cell_p - crop_p
    k_subtracted = cell_k - crop_k

    # Residue returns based on the crop's residue fraction
    n_returned = crop_n * residue_fraction + crop.n_fix
    p_returned = crop_p * residue_fraction
    k_returned = crop_k * residue_fraction

    # Fertilization returns based on the fertilization level
    if fertilization == 0:
        n_fertilization_returned = 0
        p_fertilization_returned = 0
        k_fertilization_returned = 0
    elif fertilization == 1:
        n_fertilization_returned = crop_n * 0.3
        p_fertilization_returned = crop_p * 0.3
        k_fertilization_returned = crop_k * 0.3
    elif fertilization == 2:
        n_fertilization_returned = crop_n * 0.6
        p_fertilization_returned = crop_p * 0.6
        k_fertilization_returned = crop_k * 0.6
    elif fertilization == 3:
        n_fertilization_returned = crop_n 
        p_fertilization_returned = crop_p
        k_fertilization_returned = crop_k

    total_n = cell_n - n_subtracted + n_returned + n_fertilization_returned
    total_p = cell_p - p_subtracted + p_returned + p_fertilization_returned
    total_k = cell_k - k_subtracted + k_returned + k_fertilization_returned

    cell.n = max(0.0, total_n)
    cell.p = max(0.0, total_p)
    cell.k = max(0.0, total_k)


def update_soil_moisture_after_crop(sow: int, harvest: int, cell: Cell, climate: Climate):
    """
    Updates soil moisture for a cell based in:
    - rain (mm),
    - evapotranspiration (mm)
    - relative humidity (%)
    """
    monthly_rain = climate.get_rain(sow, harvest)
    monthly_evap = climate.get_evap(sow, harvest)
    monthly_rh = climate.get_rh(sow, harvest)

    for rain, evap, rh in zip(monthly_rain, monthly_evap, monthly_rh):
        # Price restriction RH [0.0, 1.0]
        rh = min(max(rh, 0.0), 1.0)

        # Calculation of actual evaporation, taking into account relative humidity
        evap_effective = evap * (1.1 - rh)

        delta = rain - evap_effective

        cell.soil_moisture += delta 
    




    