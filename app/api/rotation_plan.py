from pydantic import BaseModel
from typing import List
from fastapi import APIRouter

class RotationInfo(BaseModel): 
    crops: List[str]
    texture: str
    irrigation: str
    nitrogen: float
    phosphorus: float
    potassium: float
    pH: float
    past_crops: List[str]
    effective_pairs: List[List[str]]
    uneffective_pairs: List[List[str]]
    years: int

router = APIRouter()

@router.post("/rotation-plan")
async def create_rotation_plan(rotation_info: RotationInfo):
    print("Received rotation info:", rotation_info)