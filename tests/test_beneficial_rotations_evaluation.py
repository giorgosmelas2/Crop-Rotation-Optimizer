import pytest
from tests.conftest import make_dummy_crop
from app.ml.evaluation.beneficial_rotations_evaluator import beneficial_rotations_evaluation
import app.ml.evaluation.beneficial_rotations_evaluator as eval_mod

@pytest.fixture
def crop_A():
    return make_dummy_crop(name="A")

@pytest.fixture
def crop_B():
    return make_dummy_crop(name="B")


# Test 1: exact match without past_crops
@pytest.mark.benefial_rotations
def test_exact_match_without_past(monkeypatch, crop_A, crop_B):
    monkeypatch.setattr(
        eval_mod,
        "get_beneficial_rotations",
        lambda: [["A", "B"]]
    )

    score = beneficial_rotations_evaluation([crop_A, crop_B], past_crops=[])
    assert score == 1.0


# Test 2: no match at all 
@pytest.mark.benefial_rotations
def test_no_match(monkeypatch, crop_A, crop_B):
    monkeypatch.setattr(eval_mod, "get_beneficial_rotations", lambda: [["X", "Y"]])
    score = beneficial_rotations_evaluation([crop_A, crop_B], past_crops=[])
    assert score == 0.0


# Test 3: multiple windows, some matches 
@pytest.mark.benefial_rotations
def test_multiple_windows_some_match(monkeypatch, crop_A, crop_B):
    monkeypatch.setattr(eval_mod, "get_beneficial_rotations", lambda: [["A", "B"]])
    crops = [crop_A, crop_B, crop_A, crop_B]
    score = beneficial_rotations_evaluation(crops, past_crops=[])
    # windows = len(crops) - 2 + 1 = 3, matches at pos 0 & 2 → 2/3
    assert pytest.approx(2/3, rel=1e-3) == score


# Test 4: with past_crops prefix 
@pytest.mark.benefial_rotations
def test_with_past_crops(monkeypatch, crop_A, crop_B):
    monkeypatch.setattr(eval_mod, "get_beneficial_rotations", lambda: [["X", "A", "B"]])
    score = beneficial_rotations_evaluation([crop_A, crop_B], past_crops=["X"])
    assert pytest.approx(1.0) == score