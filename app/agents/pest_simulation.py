from random import  sample, uniform
import math
from app.agents.pest_agent import PestAgent
from app.ml.core_models.field import Field 

class PestSimulationManager: 
    def __init__(self, pest_agents: list[PestAgent], past_pest_agents: list[PestAgent]):
        self.pest_agents = pest_agents
        self.past_pest_agents = past_pest_agents
        self.agents_by_name = {agent.name: agent for agent in pest_agents}

    def initialize_past_pest_agents(self, field: Field):
        """
        Initialize pest agents in the field grid by placing them randomly in cells.
        """
        rows = field.grid.rows
        cols = field.grid.cols
        total_cells = rows * cols
        cells_with_pests = math.ceil(total_cells * 0.1)

        all_coords = [
            (r, c)
            for r, row in enumerate(field.grid.cell_grid)
            for c in range(len(row))
        ]
        chosen = sample(all_coords, min(cells_with_pests, total_cells))

        for (r, c) in chosen:
            cell = field.grid.cell_grid[r][c]
            for past_agent in self.past_pest_agents:
                if not cell.has_this_pest(past_agent.name):
                    new_pest = PestAgent(
                        name=past_agent.name,
                        affected_crops=past_agent.affected_crops,
                        affected_families=past_agent.affected_families,
                        affected_orders=past_agent.affected_orders,
                        lifespan=uniform(0.1, 1.0),
                        row = r,
                        col = c
                    )
                    cell.pests.append(new_pest)
                    cell.pest_names.add(new_pest.name)

    def initialize_pest_agents(self, field: Field):
        """
        Adjust pest pressure based on the past crops planted by the user,
        simulating pre-existing pest presence.
        """
        rows = field.grid.rows
        cols = field.grid.cols
        total_cells = rows * cols
        cells_with_pests = math.ceil(total_cells * 0.2)

        all_coords = [
            (r, c)
            for r, row in enumerate(field.grid.cell_grid)
            for c in range(len(row))
        ]
        chosen = sample(all_coords, min(cells_with_pests, total_cells))

        for(r, c) in chosen:
            cell = field.grid.cell_grid[r][c]
            pest_name = cell.current_crop.pest
            pest_agent = self.agents_by_name.get(pest_name)
            if pest_agent is None:
                continue
            if not cell.has_this_pest(pest_agent.name):
                new_pest = PestAgent(
                    name=pest_agent.name,
                    affected_crops=pest_agent.affected_crops,
                    affected_families=pest_agent.affected_families,
                    affected_orders=pest_agent.affected_orders,
                    lifespan=uniform(0.1, 1.0),
                    row = r,
                    col = c
                )
                cell.pests.append(new_pest)
                cell.pest_names.add(new_pest.name)
 
    def step(self, field: Field):
        for cell in field.grid.get_all_cells():
            for pest in cell.pests[:]:  # copy for safe removal
                if pest.is_alive():
                    pest.apply_effect(cell)
                    pest.update_lifespan(cell)
                    if pest.is_alive():  # may have died from lifespan update
                        pest.spread(field)
                    else:
                        cell.pests.remove(pest)
                        cell.pest_names.discard(pest.name)
                else:
                    cell.pests.remove(pest)
                    cell.pest_names.discard(pest.name)