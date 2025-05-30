from pydantic import BaseModel
from typing import List
from fastapi import APIRouter

class CropPair(BaseModel):
    crop1: str
    crop2: str
    value: int

class RotationInfo(BaseModel): 
    crops: List[str]
    area: float
    texture: str
    irrigation: str
    nitrogen: float
    phosphorus: float
    potassium: float
    pH: float
    past_crops: List[str]
    effective_pairs: List[CropPair]
    uneffective_pairs: List[CropPair]
    years: int

router = APIRouter()

@router.post("/rotation-info")
async def create_rotation_plan(rotation_info: RotationInfo):
    print("Received rotation info:", rotation_info)