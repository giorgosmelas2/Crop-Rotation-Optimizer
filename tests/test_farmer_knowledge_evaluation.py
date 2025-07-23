import pytest
from app.ml.core_models.farmer_knowledge import FarmerKnowledge
from app.models.crop_pair import CropPair
from app.ml.evaluation.farmer_knowledge_evaluator import farmer_knowledge_evaluation
from tests.conftest import make_dummy_crop

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