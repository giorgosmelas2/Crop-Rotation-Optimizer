import pytest
from app.ml.core_models.economics import Economics
from app.ml.simulation_logic.simulation import simulate_crop_rotation
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.ml.core_models.climate import Climate
from app.services.required_machinery_service import get_required_machinery

from tests.test_helpers import make_dummy_crop, dummy_field

def test_smulation_runs_successfully(dummy_field): 
    # Fake crops
    crop1 = make_dummy_crop(name="Καλαμπόκι", id=1, pest="worm")
    crop2 = make_dummy_crop(name="Ηλίανθος", id=2, pest="aphid")

    crops = [crop1, crop2]

    # Fake climate
    climate = Climate