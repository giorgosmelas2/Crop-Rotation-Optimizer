from app.agents.pest_agent import PestAgent
from app.ml.grid.field_grid import FieldGrid
from app.ml.core_models.crop import Crop

class PestSimulationManager: 
    def __init__(self, pest_agents: list[PestAgent]):
        self.pest_agents = pest_agents
        self.agents_by_name = {agent.name: agent for agent in pest_agents}


    def step(self, field: FieldGrid):
        for row in range(field.rows):
            for col in range(len(field.grid[row])):
                cell = field.get_cell(row, col)
                crop = cell.current_crop

                if not crop:
                    continue

                pest = crop.pest
                agent = self.agents_by_name.get(pest)
                if not agent:
                    continue 

                new_positions = agent.spread(field, field.rows, field.cols)
                for r, c in new_positions:
                    neighbor_cell = field.get_cell(r, c)
                    agent.apply_effects(neighbor_cell)

                agent.update_lifespan(crop.family, crop.name)

                agent.decay(field)
