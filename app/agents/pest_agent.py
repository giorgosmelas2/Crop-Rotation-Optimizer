from app.ml.grid.field_grid import FieldGrid
from app.ml.grid.cell import Cell

class PestAgent: 
    def __init__(
            self,
            name: str,
            affected_crops: list[str],
            affected_families: list[str],
            row: int,
            col: int,
            lifespan: int = 3,
            spread_rate_same_family: float = 0.3,
            spread_rate_other: float = 0.1,
            decay_rate: float = 0.05,
        ):
            self.name = name
            self.affected_crops = affected_crops
            self.affected_families = affected_families

            self.row = row 
            self.col = col
            self.lifespan = lifespan

            self.spread_rate_same_family = spread_rate_same_family
            self.spread_rate_other = spread_rate_other
            self.decay_rate = decay_rate

    def is_alive(self) -> bool:
        return self.lifespan > 0
    
    def update_lifespan(self, current_crop_family: str, current_crop_name: str):
         """
         Dicrease the lifespan if there is no suitable crop for the pest 
         """
         if current_crop_name not in self.affected_crops and current_crop_family not in self.affected_families:
            self.lifespan -= 1

    
    def spread(self, field: FieldGrid, max_rows, max_cols) -> list:
        """
        Returns a list with the positions where the agent can spread
        """
        new_positions = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_r, new_c = self.row + dr, self.col + dc
            if 0 <= new_r < max_rows and 0 <= new_c < max_cols:
                cell = field.get_cell(new_r, new_c)
                crop = cell.current_crop
                crop_name = crop.name
                crop_family = crop.family

                if crop_name in self.affected_crops:
                    chance = self.spread_rate_same_family
                elif crop_family in self.affected_families:
                    chance = self.spread_rate_other
                else:
                    chance = 0.0

                from random import random
                if random() < chance:
                    new_positions.append((new_r, new_c))

        return new_positions
    
    def apply_effects(self, cell: Cell):
        """
        Effects the cell increasing the pest_pressure
        """
        crop = cell.current_crop
        if crop.name in self.affected_crops:
            cell.pest_pressure = min(cell.pest_pressure + 0.15, 1.0)
        elif crop.family in self.affected_families:
            cell.pest_pressure = min(cell.pest_pressure + 0.08, 1.0)


    def decay(self, field: FieldGrid):
        """
        Reduces pest pressure in cells where the pest is not supported.
        """
        for row in range(field.rows):
            for col in range(len(field.grid[row])):
                cell = field.get_cell(row, col)
                crop = cell.current_crop

                crop_name = crop.name
                crop_family = crop.family

                if crop_name not in self.affected_crops and crop_family not in self.affected_families:
                    cell.pest_pressure = max(cell.pest_pressure - self.decay_rate, 0.0)

        
    def __repr__(self):
        return f"<PestAgent {self.name}>"