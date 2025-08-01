from app.ml.core_models.climate import Climate


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
        """
        Calculates temperature stress on the crop during its growing season.

        Returns a value from 0 (no stress) to 1 (extreme stress) based on how 
        climate temperatures deviate from the crop's optimal and tolerable ranges.
        """
        # Get the temperature values during the crop's growth period
        sow = self.sow_month
        harvest = self.harvest_month
        tmins = climate.get_tmin(sow, harvest)
        tmaxs = climate.get_tmax(sow, harvest)

        total = 0.0 # Sum of stress values across months

        for tmin, tmax in zip(tmins, tmaxs):
            # Case 1: Extreme cold or heat beyond survivable limit
            if tmin < self.t_min - 5 or tmax > self.t_max + 5:
                return 1.0
            # Case 2: Ideal temperature range (no stress)
            elif self.t_opt_min <= tmin <= self.t_opt_max and \
                self.t_opt_min <= tmax <= self.t_opt_max:
                continue
            # Case 3: Within tolerable range but outside optimal
            elif self.t_min <= tmin <= self.t_max and self.t_min <= tmax <= self.t_max:
                # Calculate deviation from optimal temperatures
                dev_min = max(self.t_opt_min - tmin, tmin - self.t_opt_max, 0)
                dev_max = max(self.t_opt_min - tmax, tmax - self.t_opt_max, 0)
                stress = (dev_min + dev_max) / (2 * (self.t_opt_max - self.t_opt_min))

                # Apply penalty curve based on how far it is from optimal
                if (
                    self.t_min <= tmin <= self.t_opt_min and self.t_min <= tmax <= self.t_opt_min
                ) or (
                    self.t_opt_max <= tmin <= self.t_max and self.t_opt_max <= tmax <= self.t_max
                ):
                    stress **= 1.3
                else:
                    stress **= 1.1   
            # Case 4: Outside tolerable range but not catastrophic
            else:
                dev_min = max(self.t_min - tmin, tmin - self.t_max, 0)
                dev_max = max(self.t_min - tmax, tmax - self.t_max, 0)
                normalized  = (dev_min + dev_max) / (2 * (self.t_max - self.t_min))
                stress = normalized ** 1.5
              
            total += stress

        if harvest > sow:
            months = harvest - sow + 1
        else:
            months = (12 - sow + 1) + harvest 
        return min(total / months, 1.0) # Normalize and cap stress at 1.0

    def get_rain_stress(self, climate: Climate) -> float:
        """
        Calculates rainfall stress on the crop during its growing season.

        Returns a value between 0 (no stress) and 1 (maximum stress), 
        based on how the total seasonal rainfall compares to the crop's 
        acceptable rainfall range.
        """
        # Get sowing and harvesting months for slicing the climate data
        sow = self.sow_month
        harvest = self.harvest_month

        # Calculate total rainfall during the growing season
        total_rain = sum(climate.get_rain(sow, harvest))

        # If rainfall is within acceptable range → no stress
        if self.rain_min_mm <= total_rain <= self.rain_max_mm:
            return 0.0

        # If rainfall is below the minimum requirement    
        if total_rain < self.rain_min_mm:
            diff = self.rain_min_mm - total_rain
            range_ = self.rain_max_mm - self.rain_min_mm or 1  
            stress = diff / range_    
        # If rainfall exceeds the maximum tolerable value
        else:
            diff = total_rain - self.rain_max_mm
            range_ = self.rain_max_mm - self.rain_min_mm or 1
            stress = diff / range_

        # Cap the stress to a maximum of 1.0
        return min(stress, 1.0)

    def get_moisture_stress(self, cell) -> float:
        """
        Calculates moisture stress for the crop based on irrigation level 
        and available soil moisture in the cell.

        Returns a float between 0 (no stress) and 1 (maximum stress).
        """
        # Mapping of irrigation level to water availability reduction factor.
        irrigation_effect = {
            0: 1.0, # no etc covered from irrigation
            1: 0.6, # 40% of etc coverted from irrigation
            2: 0.3, # 70% coverted from irrigation
            3: 0.0 # 100% coverted from irrigation
        }

        irrigation_factor = irrigation_effect.get(cell.irrigation, 1.0)
        required_water = self.etc_mm * irrigation_factor # Decrease required water based on irrigation

        # If no water is required (e.g., full irrigation), no stress
        if required_water == 0:
            return 0.0
         
        # If the soil has enough moisture to meet the demand
        if cell.soil_moisture >= required_water:
            cell.soil_moisture -= required_water
            return 0.0
        
        # If moisture is not enough → calculate moisture deficit
        defict = required_water - cell.soil_moisture
        stress = defict / required_water

        return min(max(stress, 0.0),1.0)
        







