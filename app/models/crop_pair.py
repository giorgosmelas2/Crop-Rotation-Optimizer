from pydantic import BaseModel

class CropPair(BaseModel):
    crop1: str
    crop2: str
    value: int 
