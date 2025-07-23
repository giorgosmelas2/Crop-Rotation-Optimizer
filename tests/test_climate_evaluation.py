import pytest
from app.ml.core_models.climate import Climate
from app.ml.evaluation.climate_evaluator import climate_evaluation

@pytest.mark.climate
def test_climate_perfect_match(dummy_crop):
    # Climate exactly inside the limits
    climate = Climate(
        monthly_tmin=[dummy_crop.t_opt_min] * 12,
        monthly_tmax=[dummy_crop.t_opt_max] * 12,
        monthly_rain=[50] * 12,
        monthly_evap=[50.0] * 12,      
        monthly_rh=[0.6] * 12  
    ) 
    score = climate_evaluation(climate, dummy_crop)
    assert pytest.approx(score, rel=1e-3) == 1.0

@pytest.mark.climate
def test_climate_out_of_range_low_temp(dummy_crop):
    # Very low Tmin value
    climate = Climate(
        monthly_tmin=[dummy_crop.t_min - 10] * 12,
        monthly_tmax=[dummy_crop.t_max] * 12,
        monthly_rain=[dummy_crop.rain_min_mm] * 12,
        monthly_evap=[50.0] * 12,
        monthly_rh=[0.6] * 12
    )
    score = climate_evaluation(climate, dummy_crop)
    assert score < 1.0
    assert score >= 0.0

@pytest.mark.climate
def test_climate_frost_stress(dummy_crop):
    # Too low temperatures
    climate = Climate(
        monthly_tmin=[dummy_crop.t_min - 10] * 12,
        monthly_tmax=[dummy_crop.t_min - 5] * 12,
        monthly_rain=[50] * 12,
        monthly_evap=[30.0] * 12,
        monthly_rh=[0.5] * 12
    )

    stress = dummy_crop.get_temperature_stress(climate)
    assert stress == 1.0


@pytest.mark.climate
def test_climate_heatwave_stress(dummy_crop):
    # Too low temperatures
    climate = Climate(
        monthly_tmin=[dummy_crop.t_max + 10] * 12,
        monthly_tmax=[dummy_crop.t_max + 5] * 12,
        monthly_rain=[50] * 12,
        monthly_evap=[30.0] * 12,
        monthly_rh=[0.5] * 12
    )

    stress = dummy_crop.get_temperature_stress(climate)
    assert stress == 1.0
