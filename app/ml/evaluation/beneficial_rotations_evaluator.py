from app.ml.core_models.crop import Crop
from app.services.beneficial_rotations_service import get_beneficial_rotations

def beneficial_rotations_evaluation(crops: list[Crop], past_crops: list[str]) -> float:
    beneficial_rotations = get_beneficial_rotations()
    last_crop = past_crops[-1] # Only the last crop
    crop_names = [last_crop] + [crop.name for crop in crops]
    total_benefial_sequences = 0
    total_windows = 0

    for rotation in beneficial_rotations:
        rot_len = len(rotation)
        max_start = len(crop_names) - rot_len + 1
        total_windows += max(0, max_start)
        for i in range(max_start):
            if crop_names[i:i + rot_len] == rotation:
                total_benefial_sequences += 1

    if total_windows == 0:
        return 0.0

    return total_benefial_sequences / total_windows