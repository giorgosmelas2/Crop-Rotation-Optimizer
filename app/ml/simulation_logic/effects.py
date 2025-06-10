from app.ml.grid.cell import Cell
from app.ml.core_models.crop import Crop

def update_soil_after_crop(crop: Crop, cell: Cell): 
    """
    Update the soil nutrients in a cell after a crop is harvested.
    Args:
        crop (Crop): The crop that was harvested.
        cell (Cell): The cell where the crop was grown.
    Returns:
        None: The function modifies the cell's nutrient values in place.
    """
    # Nutrient subtractions based on the crop's nutrient uptake
    n_subtracted = cell.n - crop.n
    p_subtracted = cell.p - crop.p
    k_subtracted = cell.k - crop.k

    # Residue returns based on the crop's residue fraction
    n_returned = crop.n * crop.residue_fraction + crop.n_fix
    p_returned = crop.p * crop.residue_fraction
    k_returned = crop.k * crop.residue_fraction

    # Fertilization returns based on the fertilization level
    if cell.fertilization == 0:
        n_fertilization_returned = 0
        p_fertilization_returned = 0
        k_fertilization_returned = 0
    elif cell.fertilization == 1:
        n_fertilization_returned = crop.n * 0.3
        p_fertilization_returned = crop.p * 0.3
        k_fertilization_returned = crop.k * 0.3
    elif cell.fertilization == 2:
        n_fertilization_returned = crop.n * 0.6
        p_fertilization_returned = crop.p * 0.6
        k_fertilization_returned = crop.k * 0.6
    elif cell.fertilization == 3:
        n_fertilization_returned = crop.n 
        p_fertilization_returned = crop.p
        k_fertilization_returned = crop.k

    total_n = cell.n - n_subtracted + n_returned + n_fertilization_returned
    total_p = cell.p - p_subtracted + p_returned + p_fertilization_returned
    total_k = cell.k - k_subtracted + k_returned + k_fertilization_returned

    cell.n = max(0.0, total_n)
    cell.p = max(0.0, total_p)
    cell.k = max(0.0, total_k)




    