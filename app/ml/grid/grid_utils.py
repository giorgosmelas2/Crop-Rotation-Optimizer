from app.ml.core_models.field_state import FieldState

def create_default_cell_data(field_state: FieldState) -> dict:
    return {
        "n": field_state.n,
        "p": field_state.p,
        "k": field_state.k,
        "ph": field_state.ph,
        "soil_type": field_state.soil_type,
        "crop": None,
        "yield_": 0.0,
        "pest_pressure": 0.0,
        "history": [],
    }