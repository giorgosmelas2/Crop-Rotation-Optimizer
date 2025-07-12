import pandas as pd

class Climate():
    def __init__(
            self,
            monthly_tmin: list[float], 
            monthly_tmax: list[float], 
            monthly_rain: list[float],
            monthly_evap: list[float],
            monthly_rh: list[float],
        ):

        self.monthly_tmin = monthly_tmin
        self.monthly_tmax = monthly_tmax
        self.monthly_rain = monthly_rain
        self.monthly_evap = monthly_evap
        self.monthly_rh = monthly_rh

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "Climate":
        return cls(
            monthly_tmin=df['tmin'].tolist(),
            monthly_tmax=df['tmax'].tolist(),
            monthly_rain=df['rain'].tolist(),
            monthly_evap=df['evap'].tolist(),
            monthly_rh=df['rh'].tolist()
        )
    
    # Get methods that returns the values between sowing and harvesting months
    def get_tmin(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_tmin[sow:harvest]
    
    def get_tmax(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_tmax[sow:harvest]
    
    def get_rain(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_rain[sow:harvest]
    
    def get_evap(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_evap[sow:harvest]
    
    def get_rh(self, sow: int, harvest: int) -> list[float]:
        return self.monthly_rh[sow:harvest]    
 
            
    
        

