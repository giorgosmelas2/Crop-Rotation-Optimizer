from app.models.crop_pair import CropPair

class FarmerKnowledge():
    def __init__(self, effective_pairs: list[CropPair], uneffective_pairs: list[CropPair], past_crops: list[str]):
        self.effective_pairs = effective_pairs
        self.uneffective_pairs = uneffective_pairs
        self.past_crops = past_crops

    def __str__(self):
        return "FarmerKnowledge(\n" + "\n".join([
            f"effecrive pairs = {self.effective_pairs}",
            f"uneffective pairs = {self.uneffective_pairs}", 
        ]) + "\n)"
