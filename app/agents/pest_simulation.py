from random import randint
import math
from app.agents.pest_agent import PestAgent
from app.ml.core_models.field import Field 

class PestSimulationManager: 
    def __init__(self, pest_agents: list[PestAgent], past_pest_agents: list[PestAgent]):
        self.pest_agents = pest_agents
        self.past_pest_agents = past_pest_agents
        self.agents_by_name = {agent.name: agent for agent in pest_agents}

    def initialize_pest_agents(self, infection_rate: float, field: Field):
        """
        Initialize pest agents in the field grid by placing them randomly in cells.
        """

        total_cells = field.grid.rows * field.grid.cols
        cells_with_pests = math.ceil(total_cells * infection_rate)

        for _ in range(cells_with_pests):
            row = randint(0, field.grid.rows - 1)
            col = randint(0, len(field.grid.cell_grid[row]) - 1)
            cell = field.grid.get_cell(row, col)

            pest = self.agents_by_name.get(cell.current_crop.pest)

            while cell.has_this_pest(pest.name):
                row = randint(0, field.grid.rows - 1)
                col = randint(0, len(field.grid.cell_grid[row]) - 1)
                cell = field.grid.get_cell(row, col)

                pest = self.agents_by_name.get(cell.current_crop.pest)
            
            new_pest = PestAgent(
                name=pest.name,
                affected_crops=pest.affected_crops,
                affected_families=pest.affected_families,
                affected_orders=pest.affected_orders,
                lifespan=pest.lifespan,
                spread_rate_same_family=pest.spread_rate_same_family,
                spread_rate_same_order=pest.spread_rate_same_order,
                decay_rate=pest.decay_rate,
                spread_chance=pest.spread_chance
            )
            new_pest.row = row
            new_pest.col = col
            cell.pests.append(new_pest)
            
            print(f"Initialized pest {pest.name} at ({row}, {col})")


    def initialize_past_pest_agents(self, field: Field):
        """
        Adjust pest pressure based on the past crops planted by the user,
        simulating pre-existing pest presence.
        """
        for _ in range(len(self.past_pest_agents)):
            self.initialize_pest_agents(0.1, field)
 
    def step(self, field: Field):
        for row in range(field.grid.rows):
            for col in range(len(field.grid.cell_grid[row])):
                cell = field.grid.get_cell(row, col)
                for pest in cell.pests[:]:  # copy for safe removal
                    if pest.is_alive():
                        pest.apply_effect(cell)
                        pest.update_lifespan(cell)
                        if pest.is_alive():  # may have died from lifespan update
                            pest.spread(cell, field)
                        else:
                            print(f"Pest {pest.name} at ({row}, {col}) died after lifespan update.")
                            cell.pests.remove(pest)
                    else:
                        print(f"Pest {pest.name} at ({row}, {col}) has already died.")
                        cell.pests.remove(pest)