import pytest
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.models.crop_pair import CropPair
from app.ml.evaluation.climate_evaluator import climate_evaluation
from app.ml.evaluation.crop_rotation_evaluator import crop_rotation_evaluation
from app.ml.evaluation.farmer_knowledge_evaluator import farmer_knowledge_evaluation
from app.ml.core_models.climate import Climate
from tests.conftest import make_dummy_crop
"""
---------------------------------
    CLIMATE EVALUATOR TESTS
---------------------------------
"""
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


"""
----------------------------
    CROP ROTATION TESTS
----------------------------
"""
# Ideal rotation: each root depth changes, and in between there are legumes
@pytest.mark.crop_roatation
def test_ideal_rotation_with_legumes():
    crops = [
        make_dummy_crop(root_depth_cm=80, is_legume=False),
        make_dummy_crop(root_depth_cm=120, is_legume=True),
        make_dummy_crop(root_depth_cm=50, is_legume=False),
    ]
    score = crop_rotation_evaluation(crops)
    assert score == pytest.approx(1.0)

# No depth variation, all the same and no legumes
@pytest.mark.crop_roatation
def test_no_rotation_and_no_legumes():
    crops = [
        make_dummy_crop(root_depth_cm=100, is_legume=False),
        make_dummy_crop(root_depth_cm=100, is_legume=False),
        make_dummy_crop(root_depth_cm=100, is_legume=False),
    ]
    score = crop_rotation_evaluation(crops)
    assert score < 0.3

# Good depth variation but no legume
@pytest.mark.crop_roatation
def test_good_root_rotation_but_no_legumes():
    crops = [
        make_dummy_crop(root_depth_cm=80, is_legume=False),
        make_dummy_crop(root_depth_cm=130, is_legume=False),
        make_dummy_crop(root_depth_cm=50, is_legume=False),
    ]
    score = crop_rotation_evaluation(crops)
    assert 0.2 < score < 0.6

# Poor depth variation but with legumes that break the chain
@pytest.mark.crop_roatation
def test_poor_root_rotation_but_good_legumes():
    crops = [
        make_dummy_crop(root_depth_cm=100, is_legume=False),
        make_dummy_crop(root_depth_cm=100, is_legume=True),
        make_dummy_crop(root_depth_cm=100, is_legume=False),
    ]
    score = crop_rotation_evaluation(crops)
    assert 0.5 < score < 0.75

# Edge case: only one crop, must avoid division by zero
@pytest.mark.crop_roatation
def test_single_crop():
    crops = [make_dummy_crop(root_depth_cm=100, is_legume=False)]
    score = crop_rotation_evaluation(crops)
    assert 0.0 <= score <= 1.0

"""
------------------------------
    FARMER KNOWLEDGE TESTS
------------------------------
"""

@pytest.mark.farmer
def test_farmer_knowledge_with_one_effective_pair():
    fk = FarmerKnowledge(
        effective_pairs=[CropPair(crop1="Καλαμπόκι", crop2="Ηλίανθος", value=3)],
        uneffective_pairs=[],
    )
    crops = [
        make_dummy_crop(name="Ηλίανθος")
    ]
    past_crops = ["Καλαμπόκι"]
        
    score = farmer_knowledge_evaluation(fk, crops, past_crops)
    assert score == 1.0

@pytest.mark.farmer
def test_farmer_knowledge_with_one_uneffective_pair():
    fk = FarmerKnowledge(
        effective_pairs=[],
        uneffective_pairs=[CropPair(crop1="Καλαμπόκι", crop2="Ηλίανθος", value=3)],
    )
    crops = [
        make_dummy_crop(name="Ηλίανθος")
    ]
    past_crops = ["Καλαμπόκι"]
        
    score = farmer_knowledge_evaluation(fk, crops, past_crops)
    assert score == 0.0

@pytest.mark.farmer
def test_farmer_knowledge_with_unknown_pair():
    fk = FarmerKnowledge(
        effective_pairs=[],
        uneffective_pairs=[],
    )
    crops = [
        make_dummy_crop(name="Ηλίανθος"),
        make_dummy_crop(name="Καλαμπόκι")
    ]
    past_crops = ["Καλαμπόκι"]
    score = farmer_knowledge_evaluation(fk, crops, past_crops)
    assert score == 0.0

@pytest.mark.farmer
def test_farmer_knowledge_pair_reverse_order():
    fk = FarmerKnowledge(
        effective_pairs=[CropPair(crop1="Φακές", crop2="Βρώμη", value=3)],
        uneffective_pairs=[],
    )
    crops = [
        make_dummy_crop(name="Βρώμη"),
        make_dummy_crop(name="Φακές")
    ]
    past_crops = []
    score = farmer_knowledge_evaluation(fk, crops, past_crops)
    assert score == 0.0

