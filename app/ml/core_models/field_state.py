from typing import List

class FieldState: 
    def __init__(
            self,
            area: float,
            soil_type: str, 
            n: float, 
            p: float, 
            k: float, 
            ph: float, 
            irrigation: int, 
            fertilization: int, 
            spraying: int,
            past_crops: List[str]
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
        self.past_crops = past_crops

        self.validate()


    def validate(self):
        assert self.area >= 0, "Acres must be greater than 0."
        assert 0<= self.n <= 70, "Nitrogen (N) value must be between 0 and 70."
        assert 0<= self.p <= 25, "Phosphorus (P) value must be between 0 and 25."
        assert 0<= self.k <= 70, "Potassium (K) value must be between 0 and 70."
        assert 0<= self.ph <= 14, "pH value must be between 0 and 14."
        assert self.soil_type in ["clay", "clay loam", "loam", "loamy clay", "loamy sand", "sandy clay loam", "sandy loam", "silt loam"], "Invalid soil texture."
        assert self.irrigation in [-1, 0, 0.5, 0.75, 1], "Irrigation value must be -1, 0, 0.5, 0.75 or 1."
        assert self.fertilization in [-1, 0, 0.5, 0.75, 1], "Fertilization value must be -1, 0, 0.5, 0.75 or 1."
        assert self.spraying in [-1, 0, 0.5, 0.75, 1], "Spraying value must be -1, 0, 0.5, 0.75 or 1."

    def __str__(self):
        return "FieldState(\n" + "\n".join([
            f"area = {self.area}",
            f"soil_type = {self.soil_type}", 
            f"n = {self.n}", 
            f"p = {self.p}", 
            f"k = {self.k}", 
            f"ph = {self.ph}", 
            f"irrigation = {self.irrigation}", 
            f"fertilization = {self.fertilization}", 
            f"spraying = {self.spraying}", 
            f"past_crops = {self.past_crops}",
        ]) + "\n)"
    
    