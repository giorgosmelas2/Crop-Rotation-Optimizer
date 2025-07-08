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
    def growing_season(self, sowing_month: int, harvest_month: int) -> "Climate":
        return Climate(
            monthly_tmin=self.monthly_tmin[sowing_month:harvest_month],
            monthly_tmax=self.monthly_tmax[sowing_month:harvest_month],
            monthly_rain=self.monthly_rain[sowing_month:harvest_month]
        )
        

