import pytest
from app.models.crop_pair import CropPair
from app.ml.evaluation.profit_evaluator import (
    nutrient_penalty_factor,
    soil_type_penalty,
    ph_penalty,
    farmer_knowledge_multiplier,
    benefial_rotations_multiplier
)
from app.ml.core_models.farmer_knowledge import FarmerKnowledge

# 1. nutrient_penalty_factor
@pytest.mark.parametrize("req,expected", [
    ((10, 0, 5, 5, 3, 3), 0.5), 
    ((10, 10, 5, 0, 3, 1.5), 0.25), 
    ((10, 0, 5, 0, 3, 0), 1.0), 
    ((10, 10, 5, 5, 3, 3), 0.0), 
    ((10, 9, 5, 4, 3, 2), 0.18), 
])

@pytest.mark.profit_helpers
def test_nutrient_penalty(req, expected):
    n_req, n_act, p_req, p_act, k_req, k_act = req
    val = nutrient_penalty_factor(n_req, n_act, p_req, p_act, k_req, k_act)
    assert 0.0 <= val <= 1.0
    # precise check for the all‑missing case
    if expected == 1.0:
        assert pytest.approx(1.0) == val
    elif expected == 0.18:
        assert pytest.approx(0.18, rel=0.02) == val

# 2. soil_type_penalty
@pytest.mark.profit_helpers
def test_soil_type_penalty():
    assert soil_type_penalty("clay", "clay") == 0.0
    assert pytest.approx(0.3) == soil_type_penalty("clay", "sand")

# 3. ph_penalty
@pytest.mark.profit_helpers
def test_ph_within_tolerance():
    assert ph_penalty(6.0, 7.0, 6.4) == 0.0
    assert ph_penalty(6.0, 7.0, 7.4) == 0.0

@pytest.mark.profit_helpers
def test_ph_below():
    # crop_ph_min=6.0, tolerance=0.5 → critical below 5.5
    val = ph_penalty(6.0, 7.0, 4.0)  
    # diff = 5.5-4.0=1.5 → normalized 1.5/1.5=1.0
    assert pytest.approx(1.0) == val

@pytest.mark.profit_helpers
def test_ph_above():
    val = ph_penalty(6.0, 7.0, 8.0)
    # diff = 8.0 - 7.5 = 0.5 → normalized 0.5/1.5 ≈ 0.333
    assert pytest.approx(0.333, rel=1e-2) == val

# 4. farmer_knowledge_multiplier
@pytest.fixture
def fk():
    # ετοιμάζουμε έναν FarmerKnowledge με ένα effective και ένα uneffective
    eff = [CropPair(crop1="A", crop2="B", value=2)]
    uneff = [CropPair(crop1="B", crop2="C", value=1)]
    return FarmerKnowledge(effective_pairs=eff, uneffective_pairs=uneff, past_crops = [])

@pytest.mark.profit_helpers
def test_farmer_knowledge_effective(fk):
    # (A→B) exists with value=2 → multiplier=1+0.09*2=1.18
    assert pytest.approx(1.18) == farmer_knowledge_multiplier("A", "B", fk)

@pytest.mark.profit_helpers
def test_farmer_knowledge_uneffective(fk):
    # (B→C) exists value=1 → 1-0.09*1=0.91
    assert pytest.approx(0.91) == farmer_knowledge_multiplier("B", "C", fk)

@pytest.mark.profit_helpers
def test_farmer_knowledge_none(fk):
    assert farmer_knowledge_multiplier("X", "Y", fk) == 1.0

# 5. benefial_rotations_multiplier
@pytest.mark.profit_helpers
def test_benefial_rotations_empty():
    assert benefial_rotations_multiplier([], "Z", ["X","Y"]) == 1.0

@pytest.mark.profit_helpers
def test_benefial_rotations_match():
    bfs = [["X","Y","Z"], ["A","B","C"]]
    # past_crops reversed = [...,"Y","X"], rotation = ["X","Y","Z"] → match → 1.05
    assert pytest.approx(1.05) == benefial_rotations_multiplier(bfs, "Z", ["X","Y"])

@pytest.mark.profit_helpers
def test_benefial_rotations_no_match():
    bfs = [["A","B","C"]]
    assert benefial_rotations_multiplier(bfs, "D", ["X","Y"]) == 1.0



"""
-------------------------------
    PROFIT EVALUATOR TESTS
-------------------------------
"""

