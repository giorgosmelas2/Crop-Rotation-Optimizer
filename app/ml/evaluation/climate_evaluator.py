from app.ml.core_models.climate import Climate
from app.ml.core_models.crop import Crop

def climate_evaluation(climate: Climate, crop: Crop) -> float:
    """
    Returns a score ∈ [0, 1] indicating how well the climate fits the crop.
    1.0 means ideal; 0.0 means completely unsuitable.
    """
    temp_stress = crop.get_temperature_stress(climate)
    rain_stress = crop.get_rain_stress(climate)

    # Combined stress
    total_stress = (0.6 * temp_stress) + (0.4 * rain_stress)

    return max(0.0, 1.0 - total_stress)