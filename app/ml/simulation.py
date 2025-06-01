from copy import deepcopy
from typing import List, Dict
from app.ml.field_state import FieldState
from app.ml.crop import Crop
from app.ml.farmer_knowledge import FarmerKnowledge

def simulate_crop_rotation( field: FieldState, crops: List[Crop], farmer_knowledge: FarmerKnowledge, years: int) -> Dict:
    field_state = deepcopy(field)
    total_yield = 0.0
    compability_penalty = 0


