from app.ml.grid.field_grid import FieldGrid

class Field: 
    def __init__(
            self,
            total_area: float,
            grid: FieldGrid = None
        ):
        
        self.total_area = total_area
        self.grid = grid

    def __str__(self):
        return "FieldState(\n" + "\n".join([
            f"Total area = {self.total_area}",
            f"Total cells {self.grid.rows * self.grid.cols}"
        ]) + "\n)"
    
    