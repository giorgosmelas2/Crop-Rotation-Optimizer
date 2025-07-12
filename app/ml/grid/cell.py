from app.agents.pest_agent import PestAgent
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
            soil_moisture: float,
            irrigation: int,
            fertilization: int,
            spraying: int,
            crop_history: list[Crop] = None,
            pests: list[PestAgent] = None,
            pest_pressure: float = 0.0,
            crop: Crop = None,
            yield_: float = 0.0
        ):
        
        self.area = area
        self.n = n * 390 # Conversion from g/kg to kg/stremma
        self.p = p * 0.39 # Conversion from mg/kg to kg/stremma
        self.k = k * 0.39 # Conversion from mg/kg to kg/stremma
        self.ph = ph
        self.soil_type = soil_type
        self.soil_moisture = soil_moisture
        self.irrigation = irrigation
        self.fertilization = fertilization
        self.spraying = spraying
        self.current_crop = crop
        self.yield_ = yield_
        self.pests = pests or []
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
        self.crop_history.append(crop)
        self.yield_ = 0.0 

    def remove_crop(self):
        self.current_crop = None
        self.yield_ = 0.0

    def has_this_pest(self, pest_name: str) -> bool:
        if pest_name in [pest.name for pest in self.pests]:
            return True
        return False
    
    

