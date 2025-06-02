from pydantic import BaseModel
from typing import List
import pandas as pd


class Climate(BaseModel):
    monthly_tmin: List[float]
    monthly_tmax: List[float]
    monthly_rain: List[float] 

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "Climate":
        monthly_tmin = df['tmin'].tolist()
        monthly_tmax = df['tmax'].tolist()
        monthly_rain = df['rain'].tolist()
        return cls(
            monthly_tmin=monthly_tmin,
            monthly_tmax=monthly_tmax,
            monthly_rain=monthly_rain
        )
    
    # Get informations about the growing season
    def growing_season(self, sowing_month: int, harvest_month: int) -> "Climate":
        return Climate(
            monthly_tmin=self.monthly_tmin[sowing_month:harvest_month],
            monthly_tmax=self.monthly_tmax[sowing_month:harvest_month],
            monthly_rain=self.monthly_rain[sowing_month:harvest_month]
        )
        

