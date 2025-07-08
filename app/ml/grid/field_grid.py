from app.ml.grid.cell import Cell
from app.ml.core_models.crop import Crop

class FieldGrid: 
    def __init__(self, cells: list[Cell]):
        self.cells = cells
        self.cols = int(len(cells) ** 0.5)
        self.rows = int(len(cells) / self.cols) + (1 if len(cells) % self.cols > 0 else 0)

        self.cell_grid = [
            cells[i * self.cols : (i + 1) * self.cols]
            for i in range(self.rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        if 0 <= row < self.rows:
            if 0 <= col < len(self.cell_grid[row]):
                return self.cell_grid[row][col]
        raise IndexError("Cell coordinates out of bounds")
    
    # Adds a crop to the specified cell
    def sow_crop(self, row: int, col: int, crop: Crop):
        self.get_cell(row, col).apply_crop(crop)

    # Removes the crop from the specified cell
    def harvest_crop(self, row: int, col: int):
        self.get_cell(row, col).remove_crop()

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


        