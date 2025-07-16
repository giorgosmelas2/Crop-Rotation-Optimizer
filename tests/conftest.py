import pytest
from app.ml.core_models.crop import Crop
from app.ml.core_models.field import Field
from app.ml.core_models.climate import Climate
from app.ml.grid.cell import Cell

@pytest.fixture
def dummy_crop():
    return Crop(
        id=1,
        name="Σιτάρι",
        family="Poaceae",
        order="Poales",
        is_legume=False,
        root_depth_cm=100,
        etc_mm=200,
        sow_month=10,
        harvest_month=6,
        t_min=5, t_max=30, t_opt_min=12, t_opt_max=25,
        rain_min_mm=300, rain_max_mm=700,
        ph_min=6, ph_max=7.5,
        g_min=90, g_max=150,
        n=120, p=30, k=40,
        soil_type="loamy",
        residue_fraction=0.2, n_fix=0, n_ret=36, p_ret=6, k_ret=8,
        pest="Hessian fly"
    )

@pytest.fixture
def make_dummy_crop(**overrides) -> Crop:
    defaults = {
        "id": 1,
        "name": "Generic Crop",
        "family": "Testaceae",
        "order": "Testales",
        "is_legume": False,
        "root_depth_cm": 100,
        "etc_mm": 400,
        "sow_month": 10,
        "harvest_month": 5,
        "t_min": 5.0,
        "t_max": 35.0,
        "t_opt_min": 15.0,
        "t_opt_max": 25.0,
        "rain_min_mm": 200,
        "rain_max_mm": 600,
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
        "pest": "TestPest"
    }

    defaults.update(overrides)
    return Crop(**defaults)

@pytest.fixture
def dummy_field(dummy_crop):
    return Field(
        area=2.5,
        soil_type="loamy",
        n=120, p=30, k=40,
        ph=6.5,
        irrigation=2,
        fertilization=2,
        spraying=1,
        past_crops=["Κριθάρι", "Αραβόσιτος"],
        grid=None  
    )

@pytest.fixture
def dummy_climate():
    return Climate(
        monthly_tmin=[10.0]*12,
        monthly_tmax=[20.0]*12,
        monthly_rain=[300.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )

@pytest.fixture
def dummy_cell():
    return Cell(
        area=1.0,
        n=0.2,
        p=100.0,
        k=100.0,
        ph=6.5,
        soil_type="loamy",
        soil_moisture=200.0,
        irrigation=1,
        fertilization=1,
        spraying=1,
        crop_history=[],
        pests=[],
        pest_pressure=0.0,
        crop=None,
        yield_=0.0,
    )
