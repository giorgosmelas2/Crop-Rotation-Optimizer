import pytest, math
from app.agents.pest_simulation import PestSimulationManager
from app.agents.pest_agent import PestAgent
from tests.conftest import make_dummy_crop, make_dummy_pest_agent

@pytest.mark.pests
def test_is_alive_false_after_lifespan_zero():
    agent = PestAgent(name="X", affected_crops=[], affected_families=[], affected_orders=[])
    agent.lifespan = 0.0
    assert not agent.is_alive()
    agent.lifespan = -1.0
    assert not agent.is_alive()

@pytest.mark.pests
def test_apply_effect_no_crop_reduces_pressure(dummy_cell):
    dummy_cell.current_crop = None
    dummy_cell.pest_pressure = 0.5
    agent = PestAgent(name="X", affected_crops=[], affected_families=[], affected_orders=[])
    agent.decay_rate = 0.1
    agent.apply_effect(dummy_cell)
    assert dummy_cell.pest_pressure == pytest.approx(0.4)

@pytest.mark.pests
def test_apply_effect_same_crop_increases_pressure(dummy_cell):
    dummy_cell.current_crop = make_dummy_crop(name="Wheat", pest="WheatPest")
    dummy_cell.pest_pressure = 0.0
    agent = PestAgent(name="WheatPest", affected_crops=["Wheat"], affected_families=[], affected_orders=[])
    agent.spread_rate_same_crops = 0.2
    dummy_cell.spraying = 0
    agent.apply_effect(dummy_cell)
    assert dummy_cell.pest_pressure == pytest.approx(0.2)

@pytest.mark.pests
def test_update_lifespan_increases_for_same_crop(dummy_cell):
    dummy_cell.current_crop = make_dummy_crop(name="Corn", pest="CornPest")
    dummy_cell.crop_history = []
    agent = PestAgent(name="CornPest", affected_crops=["Corn"], affected_families=[], affected_orders=[])
    agent.lifespan = 1.0
    agent.lifespan_increase = 0.5
    agent.lifespan_decrease = 0.1
    dummy_cell.spraying = 0
    agent.update_lifespan(dummy_cell)
    assert not agent.lifespan > 1.0

@pytest.mark.pests
def test_spread_adds_new_agent_to_neighbor(monkeypatch, dummy_field):
    agent = PestAgent(name="P", affected_crops=[], affected_families=[], affected_orders=[])
    agent.row, agent.col = 1, 1  
    agent.spread_chance = 1.0
    monkeypatch.setattr("random.random", lambda: 0.0)

    dummy_field.grid.get_cell(1,1).pests = [agent]

    agent.spread(dummy_field)

    neighbors = [
        (0,1),(2,1),(1,0),(1,2),
        (0,0),(0,2),(2,0),(2,2)
    ]
    for r,c in neighbors:
        cell = dummy_field.grid.get_cell(r, c)
        assert any(p.name == "P" for p in cell.pests), f"no pest at ({r},{c})"

@pytest.mark.pests
def test_initialize_past_pest_agents_places_correct_number(monkeypatch, dummy_field):
    # force deterministic sample
    monkeypatch.setattr("random.sample", lambda lst, k: lst[:k])
    manager = PestSimulationManager(past_pest_agents=[make_dummy_pest_agent(name="A")], pest_agents=[])
    manager.initialize_past_pest_agents(dummy_field)
    total = sum(1 for row in dummy_field.grid.cell_grid for cell in row if any(p.name=="A" for p in cell.pests))
    # 10% of cells
    expected = math.ceil(dummy_field.grid.rows * dummy_field.grid.cols * 0.1)
    assert total == expected

@pytest.mark.pests
def test_step_calls_apply_update_and_removes_dead(monkeypatch, dummy_field, dummy_pest_manager):
    # Creates one agent who will die
    cell = dummy_field.grid.get_cell(0,0)
    agent = make_dummy_pest_agent(name="X")
    agent.lifespan = 0.0
    cell.pests = [agent]
    dummy_pest_manager.step(dummy_field)
    assert cell.pests == []
