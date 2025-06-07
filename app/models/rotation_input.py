from pydantic import BaseModel
from typing import List
from app.models.coordinates import Coordinates

class CropPair(BaseModel):
    crop1: str
    crop2: str
    value: int

class RotationInfo(BaseModel): 
    crops: List[str]
    coordinates: Coordinates
    area: float
    soil_type: str
    irrigation: int
    fertilization: int
    spraying: int
    n: float
    p: float
    k: float
    ph: float
    machinery: List[str]
    past_crops: List[str]
    effective_pairs: List[CropPair]
    uneffective_pairs: List[CropPair]
    years: int