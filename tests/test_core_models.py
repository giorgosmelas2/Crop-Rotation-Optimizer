import pytest

"""
---------------------------
        CROP TESTS
---------------------------
"""
#----- MOISTURE TESTS -----
@pytest.mark.crop
def test_moisture_stress_no_stress(dummy_crop, dummy_cell):
    # Sufficient moisture
    dummy_cell.soil_moisture = 400.0
    stress = dummy_crop.get_moisture_stress(dummy_cell)
    assert stress == 0.0

@pytest.mark.crop
def test_moisture_with_deficit(dummy_crop, dummy_cell):
    # Low mopisture
    dummy_cell.soil_moisture = 50.0
    stress = dummy_crop.get_moisture_stress(dummy_cell)
    assert 0.0 < stress <= 1.0

@pytest.mark.crop
def test_moisture_stress_severe(dummy_crop, dummy_cell):
    # Almost no moisture
    dummy_cell.soil_moisture = 0.0
    stress = dummy_crop.get_moisture_stress(dummy_cell)
    assert stress == 1.0


