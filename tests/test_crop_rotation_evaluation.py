import pytest
from tests.conftest import make_dummy_crop
from app.ml.evaluation.crop_rotation_evaluator import crop_rotation_evaluation

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

