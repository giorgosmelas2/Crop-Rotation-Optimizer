from typing import List
from app.ml.grid.cell import Cell

class FieldGrid: 
    def __int__(self, rows: int, cols: int, default_cell_data: dict):
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Cell]] = [
            [Cell(**default_cell_data) for _ in range(cols)] 
            for _ in range(rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        raise IndexError("Cell coordinates out of bounds")
    
    def set_crop(self, row: int, col: int, crop_name: str):
        self.grid[row][col].apply_crop(crop_name)

    def __str__(self):
        return f"FieldGrid({self.rows}x{self.cols})"

        