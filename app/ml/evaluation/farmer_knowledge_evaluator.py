from app.ml.core_models.farmer_knowledge import FarmerKnowledge

def farmer_knowledge_evaluation(farmer_knowledge: FarmerKnowledge, crop_names: list[str], past_crops: list[str]) -> float:
    """
    Evaluate the farmer's knowledge based on the crop's requirements and the farmer's knowledge.
    1.0 means the rotations has all of the farmers suggetions 0.0 means n'one of them
    """

    if past_crops:
        last_crop = past_crops[-1]
        crop_names.insert(0, last_crop)

    crop_pairs = list(zip(crop_names, crop_names[1:]))
    effective_pairs = {
        (pair.crop1, pair.crop2): pair.value
        for pair in farmer_knowledge.effective_pairs
    }

    uneffectibe_pairs = {
        (pair.crop1, pair.crop2): pair.value
        for pair in farmer_knowledge.uneffective_pairs
    } 

    score = 0 
    for pair in crop_pairs: 
        if pair in effective_pairs:
            score += effective_pairs[pair]
        elif pair in uneffectibe_pairs:
            score -= uneffectibe_pairs[pair]
    
    if score <= 0:
        return 0.0

    max_score_possible = len(crop_pairs) * 3  
    normalized_score = (score + max_score_possible) / (2 * max_score_possible)

    return max(0.0, min(normalized_score, 1.0))
