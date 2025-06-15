from app.agents.pest_agent import PestAgent
from app.ml.grid.field_grid import FieldGrid

class PestSimulationManager: 
    def __init__(self, pest_agents: list[PestAgent]):
        self.pest_agents = pest_agents

    def step(self, field: FieldGrid):
        for agent in self.pest_agents:
            spread_positions = agent.spread(field)
            for r, c in spread_positions:
                cell = field.get_cell(r, c)
                cell.pest_pressure = min(cell.pest_pressure + 0.1, 1.0)