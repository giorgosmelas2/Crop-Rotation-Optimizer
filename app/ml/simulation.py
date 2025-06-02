from copy import deepcopy
from typing import List, Dict
from app.ml.core_models.field_state import FieldState
from app.ml.core_models.crop import Crop
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate

def simulate_crop_rotation( field: FieldState, climate: Climate, crops: List[Crop], farmer_knowledge: FarmerKnowledge, years: int) -> Dict:
    field_state = deepcopy(field)
    total_yield = 0.0
    compability_penalty = 0


