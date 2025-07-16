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
        sow_idx = sow -1
        harvest_idx = harvest - 1

        if sow_idx <= harvest_idx:
            return self.monthly_tmin[sow_idx:harvest_idx]
        else:
            return self.monthly_tmin[sow_idx:] + self.monthly_tmin[:harvest_idx]

    
    def get_tmax(self, sow: int, harvest: int) -> list[float]:
        sow_idx = sow -1
        harvest_idx = harvest - 1

        if sow_idx <= harvest_idx:
            return self.monthly_tmax[sow_idx:harvest_idx]
        else:
            return self.monthly_tmax[sow_idx:] + self.monthly_tmax[:harvest_idx]
    
    def get_rain(self, sow: int, harvest: int) -> list[float]:
        sow_idx = sow -1
        harvest_idx = harvest - 1

        if sow_idx <= harvest_idx:
            return self.monthly_rain[sow_idx:harvest_idx]
        else:
            return self.monthly_rain[sow_idx:] + self.monthly_rain[:harvest_idx]
    
    def get_evap(self, sow: int, harvest: int) -> list[float]:
        sow_idx = sow -1
        harvest_idx = harvest - 1

        if sow_idx <= harvest_idx:
            return self.monthly_evap[sow_idx:harvest_idx]
        else:
            return self.monthly_evap[sow_idx:] + self.monthly_evap[:harvest_idx]
    
    def get_rh(self, sow: int, harvest: int) -> list[float]:
        sow_idx = sow -1
        harvest_idx = harvest - 1

        if sow_idx <= harvest_idx:
            return self.monthly_rh[sow_idx:harvest_idx]
        else:
            return self.monthly_rh[sow_idx:] + self.monthly_rh[:harvest_idx]
 
    
    def __str__(self):
        output = ["Climate data:"]
        for i in range(12):
            output.append(
                f"Month {i+1:>2}: Tmin={self.monthly_tmin[i]:>5.1f}°C, "
                f"Tmax={self.monthly_tmax[i]:>5.1f}°C, Rain={self.monthly_rain[i]:>6.1f}mm, "
                f"Evap={self.monthly_evap[i]:>6.1f}mm, RH={self.monthly_rh[i]*100:>5.1f}%"
            )
        return "\n".join(output)
            
    
        

