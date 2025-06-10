class Economics: 
    def __init__(
            self,
            crop_id: str,
            tonne_price_sell: float,
            unit_price: float, 
            units_per_acre: float,
            kg_yield_per_acre: float,
    ):
        self.crop_id = crop_id
        self.tonne_price_sell = tonne_price_sell
        self.unit_price = unit_price
        self.units_per_acre = units_per_acre
        self.kg_yield_per_acre = kg_yield_per_acre

    def __str__(self):
        return "Economics(\n" + "\n".join([
            f"Tonne price = {self.tonne_price_sell}",
            f"Unit price= {self.unit_price}",
            f"Units per acre = {self.units_per_acre}",
            f"Kg yield per acre = {self.kg_yield_per_acre}", 
        ]) + "\n)"