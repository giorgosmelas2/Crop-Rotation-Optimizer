from typing import List
from app.ml.grid.cell import Cell

class FieldGrid: 
    def __init__(self, cells: List[Cell]):
        self.cells = cells
        self.cols = int(len(cells) ** 0.5)
        self.rows = int(len(cells) / self.width) + (1 if len(cells) % self.width > 0 else 0)

        self.grid = [
            cells[i * self.cols : (i + 1) * self.cols]
            for i in range(self.rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        raise IndexError("Cell coordinates out of bounds")
    
    def set_crop(self, row: int, col: int, crop_name: str):
        self.grid[row][col].apply_crop(crop_name)

    def __str__(self):
        return f"FieldGrid({self.rows}x{self.cols})"
    
    def print_grid(self):
        for row in self.grid:
            print(" | ".join(cell.current_crop or "Empty" for cell in row))

        