from app.ml.grid.cell import Cell
from app.ml.core_models.crop import Crop

def update_soil_after_crop(crop: Crop, cell: Cell): 
    # Subtract the nutrients used by the crop from the cell's nutrients
    n_subtracted = cell.n - crop.n
    p_subtracted = cell.p - crop.p
    k_subtracted = cell.k - crop.k

    # Add residue returns to the soil
    n_returned = crop.n * crop.residue_fraction + crop.n_fix
    p_returned = crop.p * crop.residue_fraction
    k_returned = crop.k * crop.residue_fraction

    cell.n = max(0.0, cell.n - n_subtracted + n_returned)
    cell.p = max(0.0, cell.p - p_subtracted + p_returned)
    cell.k = max(0.0, cell.k - k_subtracted + k_returned)

    