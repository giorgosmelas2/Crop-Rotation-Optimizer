from app.ml.core_models.crop import Crop

def crop_rotation_evaluation(crops: list[Crop]) -> float:
    """
    Score a crop rotation on two criteria:
      • Root-depth alternation (30%): fraction of adjacent pairs differing ≥30cm.
      • Legume frequency (70%): penalize runs of ≥3 non-legumes.
    Returns a 0.0-1.0 score (1.0 if fewer than two crops).
    """
    # Avoid evaluation if less than 2 crops (no rotation can be evaluated)
    if len(crops) < 2:
        return 1.0 
    
    root_score = 0.0

    #--- Root depth alternation ---
    alternation_count = 0
    for prev, curr in zip(crops, crops[1:]):
        if abs(prev.root_depth_cm - curr.root_depth_cm) >= 30:
            alternation_count += 1
    
    root_score = alternation_count / (len(crops) - 1)

    #--- Legume bonus ---
    non_legume_streak = 0
    violations = 0
    for crop in crops:
        if crop.is_legume:
            non_legume_streak = 0
        else:
            non_legume_streak += 1
            if non_legume_streak >= 3:
                violations += 1
                non_legume_streak = 0

    
    max_violations = len(crops) // 3 or 1
    legume_score = max(0.0, 1.0 - (violations / max_violations))   
        
    
    final_score = 0.3 * root_score + 0.7 * legume_score
    return final_score