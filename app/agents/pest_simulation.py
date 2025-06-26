from app.agents.pest_agent import PestAgent
from app.ml.grid.field_grid import FieldGrid
from app.ml.core_models.crop import Crop

class PestSimulationManager: 
    def __init__(self, pest_agents: list[PestAgent]):
        self.pest_agents = pest_agents
        self.agents_by_name = {agent.name: agent for agent in pest_agents}

    def initialize_pest_pressure(self, field: FieldGrid, past_crops: list[Crop], next_crops: list[Crop]):
        """
        Adjust pest pressure based on the past crops planted by the user,
        simulating pre-existing pest presence.
        """
        first_crop_agent_name = next_crops[0].pest
        secont_crop_agent_name = next_crops[1].pest

        first_agent = self.agents_by_name.get(first_crop_agent_name)
        second_agent = self.agents_by_name.get(secont_crop_agent_name)

        increase = 0.0
        for idx, past_crop in enumerate(past_crops):
            if idx == 0: 
                target_agent = (first_agent,)
            else:
                target_agent = (first_agent, second_agent)

            for agent in target_agent:
                if past_crop.name in agent.affected_crops:
                    increase += 0.05 if idx else 0.03
                if past_crop.family in agent.affected_families:
                    increase += 0.03 if idx else 0.02

        for row in range(field.rows):
            for col in range(len(field.grid[row])):
                cell = field.get_cell(row, col)
                cell.pest_pressure += increase

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
