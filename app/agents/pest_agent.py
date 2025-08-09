from __future__ import annotations
import copy
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.ml.core_models.field import Field
    from app.ml.grid.cell import Cell

import random

SPRAYING_EFFECT_PRESSURE = { 0: 0.0, 1: 0.3, 2: 0.7, 3: 0.95 }
SPRAYING_EFFECT_LIFESPAN = { 0: 0.0, 1: 0.2, 2: 0.5, 3: 0.7 }

class PestAgent: 
    def __init__(
            self,
            name: str,  
            affected_crops: list[str],
            affected_families: list[str],
            affected_orders: list[str],
            lifespan: float = 1.0,
            row: int | None = None,
            col: int | None = None,
        ):
            self.name = name
            self.lifespan = lifespan
            # self.lifespan_increase = random.uniform(0.1, 0.2)
            # self.lifespan_decrease = random.uniform(0.1, 0.2)
            self.lifespan_increase = 0.15
            self.lifespan_decrease = 0.15
            self.affected_crops = affected_crops
            self.affected_families = affected_families
            self.affected_orders = affected_orders

            self.row = row
            self.col = col

            # self.spread_rate_same_crops = random.uniform(0.15, 0.2)
            # self.spread_rate_same_family = random.uniform(0.07, 0.12)
            # self.spread_rate_same_order = random.uniform(0.03, 0.5)
            # self.decay_rate = random.uniform(0.05, 0.09)
            # self.spread_chance = random.uniform(0.1, 0.25)
            
            self.spread_rate_same_crops = 0.2
            self.spread_rate_same_family = 0.1
            self.spread_rate_same_order = 0.05
            self.decay_rate = 0.07
            self.spread_chance = 0.2

    def is_alive(self) -> bool:
        return self.lifespan > 0.0
    
    def spread(self, field: Field):
        """
        Spread the pest agent to neighboring cells
        """
        # To decrease the run time of GA
        row = self.row
        col = self.col
        name = self.name

        neighbors = [
            (row - 1, col), # Up
            (row + 1, col), # Down
            (row, col - 1), # Left
            (row, col + 1), # Right
            # (row - 1, col - 1), # Up-Left
            # (row - 1, col + 1), # Up-Right
            # (row + 1, col - 1), # Down-Left
            # (row + 1, col + 1) # Down-Right
        ]

        rand_value = random.random()

        for n_row, n_col in neighbors:
            if 0 <= n_row < field.grid.rows:
                row_len = len(field.grid.cell_grid[n_row])
                if 0 <= n_col < row_len:
                    neighbor_cell = field.grid.cell_grid[n_row][n_col]
                    if not neighbor_cell.has_this_pest(name): 
                        if rand_value < self.spread_chance:
                            # new_pest = PestAgent(
                            #     name=name,
                                
                            #     lifespan=self.lifespan,
                            #     affected_crops=self.affected_crops,
                            #     affected_families=self.affected_families,
                            #     affected_orders=self.affected_orders,

                            #     row=n_row,
                            #     col=n_col,
                            # )
                            new_pest = self.clone_to(n_row, n_col)
                            neighbor_cell.pests.append(new_pest)
                            neighbor_cell.pest_names.add(new_pest.name)
                    

    def apply_effect(self, cell: Cell):
        """
        Apply the pest agent's effect on the field
        """
        spraying_level = cell.spraying
   
        current_crop = cell.current_crop
        if not current_crop:
            cell.pest_pressure -= self.decay_rate
            cell.pest_pressure = max(cell.pest_pressure, 0.0)
            return
        
        if current_crop.name in self.affected_crops:
            rate = self.spread_rate_same_crops
        elif current_crop.family in self.affected_families:
            rate = self.spread_rate_same_family
        elif current_crop.order in self.affected_orders:
            rate = self.spread_rate_same_order
        else:
            decay = self.decay_rate * (1 + SPRAYING_EFFECT_PRESSURE[spraying_level])
            cell.pest_pressure = max(cell.pest_pressure - decay, 0.0)
            return

        # Decrease of the spread rate based on spraying level
        reduction = SPRAYING_EFFECT_PRESSURE[spraying_level] * rate
        cell.pest_pressure += rate - reduction
        cell.pest_pressure = min(cell.pest_pressure, 1.0)
                        
    def update_lifespan(self, cell: Cell):
        # To decrease the run time of GA
        lifespan = self.lifespan
        lifespan_increase = self.lifespan_increase
        lifespan_decrease = self.lifespan_decrease
        affected_crops = self.affected_crops
        affected_families = self.affected_families
        affected_orders = self.affected_orders

        spraying_level = cell.spraying
        current_crop = cell.current_crop 
        past_crop = cell.crop_history[-1] if len(cell.crop_history) >= 1 else None
        pre_past_crop = cell.crop_history[-2] if len(cell.crop_history) >= 2 else None

        spraying_decrease = SPRAYING_EFFECT_LIFESPAN[spraying_level] * lifespan_decrease
        lifespan -= spraying_decrease

        if lifespan > 0.0:
            if current_crop:
                if current_crop.name in affected_crops:
                    lifespan += lifespan_increase
                elif current_crop.family in affected_families:
                    lifespan += lifespan_increase * 0.5
                elif current_crop.order in affected_orders:
                    lifespan += lifespan_increase * 0.25
                else:
                    lifespan -= lifespan_decrease
            else:
                lifespan -= lifespan_decrease

            if past_crop:
                if past_crop.name in affected_crops:
                    lifespan += lifespan_increase * 0.5
                elif past_crop.family in affected_families:
                    lifespan += lifespan_increase * 0.25
                elif past_crop.order in affected_orders:
                    lifespan += lifespan_increase * 0.1
            
            if pre_past_crop:
                if pre_past_crop.name in affected_crops:
                    lifespan += lifespan_increase * 0.25
                elif pre_past_crop.family in affected_families:
                    lifespan += lifespan_increase * 0.1
                elif pre_past_crop.order in affected_orders:
                    lifespan += lifespan_increase * 0.05
        
        self.lifespan = max(0.0, min(lifespan, 1.0))

    def clone_to(self, new_row: int, new_col: int) -> "PestAgent":
        clone = PestAgent(
            name=self.name,
            lifespan=self.lifespan,
            affected_crops=self.affected_crops[:],
            affected_families=self.affected_families[:],
            affected_orders=self.affected_orders[:],
            row=new_row,
            col=new_col
        )

        # Copy "behavioral" parameters
        clone.lifespan_increase = self.lifespan_increase
        clone.lifespan_decrease = self.lifespan_decrease
        clone.spread_rate_same_crops = self.spread_rate_same_crops
        clone.spread_rate_same_family = self.spread_rate_same_family
        clone.spread_rate_same_order = self.spread_rate_same_order
        clone.decay_rate = self.decay_rate
        clone.spread_chance = self.spread_chance

        return clone
            
    def __repr__(self):
        return (
            f"<PestAgent "
            f"name={self.name!r}, "
            f"row={self.row}, "
            f"col={self.col}, "
            f">"
        )