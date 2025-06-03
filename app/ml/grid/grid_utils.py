import math
from typing import List
from app.ml.core_models.field_state import FieldState
from app.ml.grid.cell import Cell


def create_default_cell_data(field_state: FieldState) -> dict:
    return {
        "n": field_state.n,
        "p": field_state.p,
        "k": field_state.k,
        "ph": field_state.ph,
        "soil_type": field_state.soil_type,
        "irrigation": field_state.irrigation,
        "fertilization": field_state.fertilization,
        "spraying": field_state.spraying,
    }

def cell_create(total_area: float, field_state: FieldState) -> List[Cell]:
    full_cells = int(total_area)
    remainder = round(total_area - full_cells, 2)

    areas = [1.0] * full_cells
    if remainder > 0:
        areas.append(remainder)

    base_data = create_default_cell_data(field_state)

    cells = []
    for area in areas:
        cell = Cell(area=area, **base_data)
        cells.append(cell)
    
    return cells
