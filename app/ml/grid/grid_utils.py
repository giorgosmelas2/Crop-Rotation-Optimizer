from app.models.rotation_input import RotationInfo
from app.ml.grid.cell import Cell

def create_default_cell_data(rotation_info: RotationInfo) -> dict:
    return {
        "n": rotation_info.n,
        "p": rotation_info.p,
        "k": rotation_info.k,
        "ph": rotation_info.ph,
        "soil_type": rotation_info.soil_type,
        "soil_moisture": 0.0,
        "irrigation": rotation_info.irrigation,
        "fertilization": rotation_info.fertilization,
        "spraying": rotation_info.spraying,
    }

def cell_create(rotation_info: RotationInfo) -> list[Cell]:
    full_cells = int(rotation_info.area)
    remainder = round(rotation_info.area - full_cells, 2)

    areas = [1.0] * full_cells
    if remainder > 0:
        areas.append(remainder)

    base_data = create_default_cell_data(rotation_info)

    cells = []
    for area in areas:
        cell = Cell(area=area, **base_data)
        cells.append(cell)
    
    return cells
