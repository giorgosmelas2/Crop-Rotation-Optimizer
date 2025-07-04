from typing import List
from app.ml.core_models.crop import Crop

class Cell:
    def __init__(
            self,
            area: float,
            n: float, 
            p: float, 
            k: float,
            ph: float, 
            soil_type: str, 
            irrigation: int,
            fertilization: int,
            spraying: int,
            crop_history: List[str] = None,
            pest_pressure: float = 0.0,
            crop: Crop = None,
            yield_: float = 0.0
        ):
        
        self.area = area
        self.n = n
        self.p = p
        self.k = k
        self.ph = ph
        self.soil_type = soil_type
        self.irrigation = irrigation
        self.fertilization = fertilization
        self.spraying = spraying
        self.current_crop = crop
        self.yield_ = yield_
        self.pest_pressure = pest_pressure
        self.crop_history = crop_history or []

    def __str__(self):
        return "Cell(\n" + "\n".join([
            f"area = {self.area}",
            f"n={self.n}", 
            f"p={self.p}", 
            f"k={self.k}", 
            f"ph={self.ph}", 
            f"soil_type={self.soil_type}",
            f"irrigation={self.irrigation}",
            f"fertilization={self.fertilization}",
            f"spraying={self.spraying}",
            f"crop_history={self.crop_history}",
            f"crop={self.current_crop.name}", 
            f"yield_={self.yield_}", 
            f"pest_pressure={self.pest_pressure}",
            ]) + "\n)"
    
    def apply_crop(self, crop: Crop):
        self.current_crop = crop
        self.crop_history.append(crop.name)
        self.yield_ = 0.0 # Reset yield when applying a new crop

    def remove_crop(self):
        self.current_crop = None
        self.yield_ = 0.0


