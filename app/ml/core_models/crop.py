class Crop:
    def __init__(
            self,
            crop_id: int,
            crop_name: str,
            family: str,
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
            ):
        
        self.crop_id = crop_id
        self.crop_name = crop_name
        self.family = family
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


    def __repr__(self):
        return "Crop(\n" + "\n".join([
            f"crop_id: {self.crop_id}",
            f"crop_name: {self.crop_name}",
            f"family: {self.family}",
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
        ]) + "\n)"
        
    def __str__(self):
        return "Crop(\n" + "\n".join([
            f"crop_id: {self.crop_id}",
            f"crop_name: {self.crop_name}",
            f"family: {self.family}",
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
        ]) + "\n)"