import pytest
from app.ml.core_models.crop import Crop
from app.ml.core_models.climate import Climate
from app.ml.core_models.field import Field

@pytest.fixture
def dummy_crop():
    return Crop(name="Σκληρό σιτάρι",family="Poaceae", sow_month=11, harvest_month=6 )

def make_dummy_crop(**overrides) -> Crop:
    defaults = {
        "id": 1,
        "name": "Σκληρό σιτάρι",
        "family": "Poaceae",
        "order": "Poales",
        "is_legume": False,
        "root_depth_cm": 150,
        "etc_mm": 500,
        "sow_month": 11,
        "harvest_month": 6,
        "t_min": 5.0,
        "t_max": 32.0,
        "t_opt_min": 13.1,
        "t_opt_max": 25.0,
        "rain_min_mm": 300,
        "rain_max_mm": 800,
        "ph_min": 6.0,
        "ph_max": 7.5,
        "g_min": 90,
        "g_max": 150,
        "n": 120.0,
        "p": 30.0,
        "k": 40.0,
        "soil_type": "loamy",
        "residue_fraction": 0.2,
        "n_fix": 0.0,
        "n_ret": 0.3,
        "p_ret": 0.2,
        "k_ret": 0.3,
        "pest": "Rust"
    }

    defaults.update(overrides)
    return Crop(**defaults)

@pytest.fixture
def dummy_field():
    return Field(
        area=5,
        soil_type="loamy",
        n=78.0,
        p=39.0,
        k=39.0,
        ph=6.5,
        fertilization=2,
        spraying=1,
        irrigation=1,
        past_crops=["Κριθάρι", "Αραβόσιτος"]
    )