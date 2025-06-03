from copy import deepcopy
from typing import List, Dict

from app.ml.core_models.field_state import FieldState
from app.ml.core_models.crop import Crop
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate

from app.ml.grid.grid_utils import cell_create

def simulate_crop_rotation( field: FieldState, climate: Climate, crops: List[Crop], farmer_knowledge: FarmerKnowledge, years: int) -> Dict:
    field_state = deepcopy(field)

    cells = cell_create(field_state.area, field_state)

    for i, cell in enumerate(cells):
        print(f"Cell {i+1}:\n{cell}\n")

    grid = FieldState(cells=cells)

    


