import pandas as pd

class Climate():
    def __init__(
            self,
            monthly_tmin: list[float], 
            monthly_tmax: list[float], 
            monthly_rain: list[float]
        ):

        self.monthly_tmin = monthly_tmin
        self.monthly_tmax = monthly_tmax
        self.monthly_rain = monthly_rain

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "Climate":
        return cls(
            monthly_tmin=df['tmin'].tolist(),
            monthly_tmax=df['tmax'].tolist(),
            monthly_rain=df['rain'].tolist()
        )
    

    
    # Get informations about the growing season
    def get_tmin(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_tmin[sow:harvest]
    
    def get_tmax(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_tmax[sow:harvest]
    
    def get_rain(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_rain[sow:harvest],
            
    
        

