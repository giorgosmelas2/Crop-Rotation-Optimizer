from pydantic import BaseModel
from typing import List

class CropPair(BaseModel):
    crop1: str
    crop2: str
    value: int 

class FarmerKnowledge():
    def __init__(self, effective_pairs: List[CropPair], uneffective_pairs: List[CropPair]):
        self.effective_pairs = effective_pairs
        self.uneffective_pairs = uneffective_pairs

    def __str__(self):
        return "FarmerKnowledge(\n" + "\n".join([
            f"effecrive pairs = {self.effective_pairs}",
            f"uneffective pairs = {self.uneffective_pairs}", 
        ]) + "\n)"
