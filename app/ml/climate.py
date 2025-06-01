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
    

