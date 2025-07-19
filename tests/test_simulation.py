import pytest
from app.ml.core_models.field import Field
from app.ml.core_models.climate import Climate
from app.ml.core_models.crop import Crop
from app.agents.pest_simulation import PestSimulationManager
from app.ml.optimization.genetic_custom import run_ga_custom

@pytest.fixture
def basic_setup():
    field = Field(total_area=4, )