import pytest
from app.ml.core_models.climate import Climate

"""
---------------------------
        CROP TESTS
---------------------------
"""
#----- MOISTURE TESTS -----
@pytest.mark.crop_moisture
def test_moisture_stress_no_stress(dummy_crop, dummy_cell):
    # Sufficient moisture
    dummy_cell.soil_moisture = 400.0
    stress = dummy_crop.get_moisture_stress(dummy_cell)
    assert stress == 0.0

@pytest.mark.crop_moisture
def test_moisture_with_deficit(dummy_crop, dummy_cell):
    # Low mopisture
    dummy_cell.soil_moisture = 50.0
    stress = dummy_crop.get_moisture_stress(dummy_cell)
    assert 0.0 < stress <= 1.0

@pytest.mark.crop_moisture
def test_moisture_stress_severe(dummy_crop, dummy_cell):
    # Almost no moisture
    dummy_cell.soil_moisture = 0.0
    stress = dummy_crop.get_moisture_stress(dummy_cell)
    assert stress == 1.0

@pytest.mark.crop_temp
def test_temperature_stress_ideal(dummy_crop, dummy_climate):
    stress = dummy_crop.get_temperature_stress(dummy_climate)
    assert stress == 0.0

@pytest.mark.crop_temp
def test_temperature_stress_middle_performance(dummy_crop):
    middle_climate = Climate(
        monthly_tmin=[10.0]*12,
        monthly_tmax=[27.0]*12,  
        monthly_rain=[300.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )
    stress = dummy_crop.get_temperature_stress(middle_climate)
    assert stress < 0.3

@pytest.mark.crop_temp
def test_temperature_stress_extreme_heat(dummy_crop):
    hot_climate = Climate(
        monthly_tmin=[20.0]*12,
        monthly_tmax=[45.0]*12,  
        monthly_rain=[300.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )
    stress = dummy_crop.get_temperature_stress(hot_climate)
    assert stress == 1.0

@pytest.mark.rain
def test_very_low_rain(dummy_crop):
    low_rain_climate = Climate(
        monthly_tmin=[20.0]*12,
        monthly_tmax=[45.0]*12,  
        monthly_rain=[500.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )
    stress = dummy_crop.get_rain_stress(low_rain_climate)
    assert stress == 1.0

@pytest.mark.rain
def test_too_much_rain(dummy_crop):
    too_much_rain_climate = Climate(
        monthly_tmin=[20.0]*12,
        monthly_tmax=[45.0]*12,  
        monthly_rain=[1000.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )
    stress = dummy_crop.get_rain_stress(too_much_rain_climate)
    assert stress == 1.0

@pytest.mark.rain
def test_middle_under_rain(dummy_crop):
    middle_under_rain_climate = Climate(
        monthly_tmin=[20.0]*12,
        monthly_tmax=[45.0]*12,  
        monthly_rain=[40.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )
    stress = dummy_crop.get_rain_stress(middle_under_rain_climate)
    assert 0.05 <= stress <= 0.2

@pytest.mark.rain
def test_middle_up_rain(dummy_crop):
    middle_up_rain_climate = Climate(
        monthly_tmin=[20.0]*12,
        monthly_tmax=[45.0]*12,  
        monthly_rain=[105.0]*12,
        monthly_evap=[50.0]*12,
        monthly_rh=[0.6]*12
    )
    stress = dummy_crop.get_rain_stress(middle_up_rain_climate)
    assert 0.05 <= stress <= 0.2