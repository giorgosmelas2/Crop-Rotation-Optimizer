from app.ml.grid.cell import Cell
from app.ml.core_models.crop import Crop
from app.ml.core_models.climate import Climate
from app.ml.simulation_logic.effects import update_soil_after_crop, update_soil_moisture_after_crop


class FieldGrid: 
    def __init__(self, cells: list[Cell]):
        self.cells = cells
        self.cols = int(len(cells) ** 0.5)
        self.rows = int(len(cells) / self.cols) + (1 if len(cells) % self.cols > 0 else 0)

        self.cell_grid = [
            cells[i * self.cols : (i + 1) * self.cols]
            for i in range(self.rows)
        ]

    def get_all_cells(self) -> list[Cell]:
        return self.cells 

    def get_cell(self, row: int, col: int) -> Cell:
        return self.cell_grid[row][col]

    # Sow crop to all cells in the field
    def sow_crop_to_all(self, crop: Crop):
        for cell in self.cells:
            cell.apply_crop(crop)

    # Harvest crop from all cells in the field
    def harvest_all(self, crop: Crop, climate: Climate):
        for cell in self.cells:
            update_soil_moisture_after_crop(crop.sow_month, crop.harvest_month, cell, climate)
            update_soil_after_crop(crop, cell)
            cell.remove_crop()


    # Returns the total area of the field
    def get_total_area(self) -> float:
        return sum(cell.area for row in self.cell_grid for cell in row)

    # Checks if the field is empty (i.e., no crops are currently planted)
    def is_field_empty(self) -> bool:
        return all(cell.current_crop is None for row in self.cell_grid for cell in row)

    def __str__(self):
        return f"FieldGrid({self.rows}x{self.cols})"
    
    def print_grid(self):
        for row in self.cell_grid:
            print(" | ".join(cell.current_crop or "Empty" for cell in row))
    
    def print_nutrients(self):
        for r, row in enumerate(self.cell_grid):
            for c, cell in enumerate(row):
                print(f"[{r},{c}] N={cell.n:.2f}, P={cell.p:.2f}, K={cell.k:.2f}, Crop={cell.current_crop}")


        