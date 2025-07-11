from app.ml.core_models.climate import Climate
from app.ml.grid.cell import Cell

class Crop:
    def __init__(
            self,
            id: int,
            name: str,
            family: str,
            order: str,
            is_legume: bool,
            root_depth_cm: int,
            etc_mm: int,
            sow_month: int,
            harvest_month: int,
            t_min: float,
            t_max: float,
            t_opt_min: float,
            t_opt_max: float,
            rain_min_mm: int,
            rain_max_mm: int,
            ph_min: float,
            ph_max: float,
            g_min: int,
            g_max: int,
            n: float, 
            p: float,
            k: float,
            soil_type: str,
            residue_fraction: float,
            n_fix: float,
            n_ret: float,
            p_ret: float,
            k_ret: float,
            pest: str
        ):
        
        self.id = id
        self.name = name
        self.family = family
        self.order = order
        self.is_legume = is_legume
        self.root_depth_cm = root_depth_cm
        self.etc_mm = etc_mm
        self.sow_month = sow_month
        self.harvest_month = harvest_month
        self.t_min = t_min
        self.t_max = t_max
        self.t_opt_min = t_opt_min
        self.t_opt_max = t_opt_max
        self.rain_min_mm = rain_min_mm
        self.rain_max_mm = rain_max_mm
        self.ph_min = ph_min
        self.ph_max = ph_max
        self.g_min = g_min
        self.g_max = g_max
        self.n = n
        self.p = p
        self.k = k
        self.soil_type = soil_type
        self.residue_fraction = residue_fraction
        self.n_fix = n_fix
        self.n_ret = n_ret
        self.p_ret = p_ret
        self.k_ret = k_ret
        self.pest = pest


    def __repr__(self):
        return "Crop(\n" + "\n".join([
            f"crop_id: {self.id}",
            f"crop_name: {self.name}",
            f"family: {self.family}",
            f"order: {self.order}",
            f"is_legume: {self.is_legume}",
            f"root_depth_cm: {self.root_depth_cm}",
            f"etc_mm: {self.etc_mm}",
            f"sow_month: {self.sow_month}",
            f"harvest_month: {self.harvest_month}",
            f"t_min: {self.t_min}",
            f"t_max: {self.t_max}",
            f"t_opt_min: {self.t_opt_min}",
            f"t_opt_max: {self.t_opt_max}",
            f"rain_min_mm: {self.rain_min_mm}",
            f"rain_max_mm: {self.rain_max_mm}",
            f"ph_min: {self.ph_min}",
            f"ph_max: {self.ph_max}",
            f"g_min: {self.g_min}",
            f"g_max: {self.g_max}",
            f"n: {self.n}",
            f"p: {self.p}",
            f"k: {self.k}",
            f"soil_type: {self.soil_type}",
            f"residue_fraction: {self.residue_fraction}",
            f"n_fix: {self.n_fix}",
            f"n_ret: {self.n_ret}",
            f"p_ret: {self.p_ret}",
            f"k_ret: {self.k_ret}",
            f"pest: {self.pest}",
        ]) + "\n)"
        
    def __str__(self):
        return "Crop(\n" + "\n".join([
            f"crop_id: {self.id}",
            f"crop_name: {self.name}",
            f"family: {self.family}",
            f"order: {self.order}",
            f"is_legume: {self.is_legume}",
            f"root_depth_cm: {self.root_depth_cm}",
            f"etc_mm: {self.etc_mm}",
            f"sow_month: {self.sow_month}",
            f"harvest_month: {self.harvest_month}",
            f"t_min: {self.t_min}",
            f"t_max: {self.t_max}",
            f"t_opt_min: {self.t_opt_min}",
            f"t_opt_max: {self.t_opt_max}",
            f"rain_min_mm: {self.rain_min_mm}",
            f"rain_max_mm: {self.rain_max_mm}",
            f"ph_min: {self.ph_min}",
            f"ph_max: {self.ph_max}",
            f"g_min: {self.g_min}",
            f"g_max: {self.g_max}",
            f"n: {self.n}",
            f"p: {self.p}",
            f"k: {self.k}",
            f"soil_type: {self.soil_type}",
            f"residue_fraction: {self.residue_fraction}",
            f"n_fix: {self.n_fix}",
            f"n_ret: {self.n_ret}",
            f"p_ret: {self.p_ret}",
            f"k_ret: {self.k_ret}",
            f"pest: {self.pest}",
        ]) + "\n)"
    
    def get_temperature_stress(self, climate: Climate) -> float:
        sow = self.sow_month
        harvest = self.harvest_month
        tmins = climate.get_tmin(sow, harvest)
        tmaxs = climate.get_tmax(sow, harvest)

        stress = 0.0
        total = 0.0
        for tmin, tmax in zip(tmins, tmaxs):
            # Ideal range
            if self.t_opt_min <= tmin <= self.t_opt_max and \
                self.t_opt_min <= tmax <= self.t_opt_max:
                continue
            # Tolerable range
            if self.t_min <= tmin <= self.t_max and self.t_min <= tmax <= self.t_max:
                # dev from the optimal
                dev_min = max(self.t_opt_min - tmin, tmin - self.t_opt_max, 0)
                dev_max = max(self.t_opt_min - tmax, tmax - self.t_opt_max, 0)
                stress = (dev_min + dev_max) / (2 * (self.t_opt_max - self.t_opt_min))

                if (
                    self.t_min <= tmin <= self.t_opt_min and self.t_min <= tmax <= self.t_opt_min
                ) or (
                    self.t_opt_max <= tmin <= self.t_max and self.t_opt_max <= tmax <= self.t_max
                ):
                    stress **= 1.3
                else:
                    stress **= 1.1   
            else:
                # Out of range
                dev_min = max(self.t_min - tmin, tmin - self.t_max, 0)
                dev_max = max(self.t_min - tmax, tmax - self.t_max, 0)
                normalized  = (dev_min + dev_max) / (2 * (self.t_max - self.t_min))
                stress = normalized ** 1.5
              
            total += stress

        months = max(harvest - sow, 1)
        return min(total / months, 1.0)

    def get_rain_stress(self, climate: Climate) -> float:
        sow = self.sow_month
        harvest = self.harvest_month
        total_rain = sum(climate.get_rain(sow, harvest))

        if self.rain_min_mm <= total_rain <= self.rain_max_mm:
            return 0.0
            
        if total_rain < self.rain_min_mm:
            diff = self.rain_min_mm - total_rain
            range_ = self.rain_max_mm - self.rain_min_mm or 1  
            stress = diff / range_
        else:
            diff = total_rain - self.rain_max_mm
            range_ = self.rain_max_mm - self.rain_min_mm or 1
            stress = diff / range_

        return min(stress, 1.0)

    def get_moisture_stress(self, cell: Cell) -> float:
        irrigation_effect = {
            0: 1.0,
            1: 0.6,
            2: 0.3,
            3: 0.0
        }

        irrigation_factor = irrigation_effect.get(cell.irrigation, 1.0)
        required_water = self.etc_mm * irrigation_factor

        if required_water == 0:
            return 0.0
        
        if cell.soil_moisture >= required_water:
            cell.soil_moisture -= required_water
            return 0.0
        
        defict = required_water - cell.soil_moisture
        stress = defict / required_water

        return min(max(stress, 0.0),1.0)
        







