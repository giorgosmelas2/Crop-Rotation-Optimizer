class FieldState: 
    def __init__(
            self,
            acres: float,
            n: float, 
            p: float, 
            k: float, 
            ph: float, 
            soil_type: str, 
            irrigation: int, 
            fertilization: int, 
            spraying: int
            ):
        
        acres = acres
        self.n = n
        self.p = p
        self.k = k
        self.ph = ph
        self.soil_type = soil_type
        self.irrigation = irrigation
        self.fertilization = fertilization
        self.spraying = spraying

        self.validate()


    def validate(self):
        assert self.acres > 0, "Acres must be greater than 0."
        assert 0<= self.n <= 70, "Nitrogen (N) value must be between 0 and 70."
        assert 0<= self.p <= 25, "Phosphorus (P) value must be between 0 and 25."
        assert 0<= self.k <= 70, "Potassium (K) value must be between 0 and 70."
        assert 0<= self.ph <= 14, "pH value must be between 0 and 14."
        assert self.soil_type in ["clay", "clay loam", "loam", "loamy clay", "loamy sand", "sandy clay loam", "sandy loam", "silt loam"], "Invalid soil texture."
        assert self.irrigation in [0, 1, 2, 3], "Irrigation value must be 0, 1, 2, or 3."
        assert self.fertilization in [0, 1, 2, 3], "Fertilization value must be 0, 1, 2, or 3."
        assert self.spraying in [0, 1, 2, 3], "Spraying value must be 0, 1, 2, or 3."