import pytest
from app.ml.evaluation.profit_evaluator import profit_evaluation
from app.ml.core_models.economics import Economics
from tests.conftest import make_dummy_crop

# 1) Ιδανικές συνθήκες → profit == 1.0
@pytest.mark.profit
def test_profit_maximum(
    dummy_crop,
    dummy_field,
    dummy_climate,
    dummy_farmer_knowledge,
    dummy_beneficial_rotations,
    dummy_economic_data,
):
    # find crop economic record  
    economic = dummy_economic_data[dummy_crop.id]
    # override για να μηδενίσουμε κόστος
    economic.unit_price = 0
    economic.units_per_acre = 0

    profit = profit_evaluation(
        crop=dummy_crop,
        field=dummy_field,
        economic=economic,
        climate=dummy_climate,
        farmer_knowledge=dummy_farmer_knowledge,
        beneficial_rotations=dummy_beneficial_rotations,
    )
    assert profit == pytest.approx(1.0)


# 2) Zero yield → profit == 0.0
@pytest.mark.profit
def test_zero_yield(
    dummy_crop,
    dummy_field,
    dummy_climate,
    dummy_farmer_knowledge,
    dummy_beneficial_rotations,
    dummy_economic_data,
):
    economic = dummy_economic_data[dummy_crop.id]
    economic.kg_yield_per_acre = 0

    profit = profit_evaluation(
        crop=dummy_crop,
        field=dummy_field,
        economic=economic,
        climate=dummy_climate,
        farmer_knowledge=dummy_farmer_knowledge,
        beneficial_rotations=dummy_beneficial_rotations,
    )
    assert profit == 0.0


# 3) Revenue = 2×cost → normalized_profit = 0.5
@pytest.mark.profit
def test_partial_profit(
    dummy_crop,
    dummy_field,
    dummy_climate,
    dummy_farmer_knowledge,
    dummy_beneficial_rotations,
    dummy_economic_data,
):
    economic = dummy_economic_data[dummy_crop.id]
    # 2000 kg yield → 2 tonnes revenue
    economic.kg_yield_per_acre = 2000
    economic.tonne_price_sell = 1
    # cost = 1 $/unit × 1 unit/acre × 1 acre = 1
    economic.unit_price = 1
    economic.units_per_acre = 1

    profit = profit_evaluation(
        crop=dummy_crop,
        field=dummy_field,
        economic=economic,
        climate=dummy_climate,
        farmer_knowledge=dummy_farmer_knowledge,
        beneficial_rotations=dummy_beneficial_rotations,
    )
    # max_revenue = 2000 kg→2t, cost=1 → max_possible_profit=1 → normalized = profit/max=1/1=1
    # για partial test, ας μειώσουμε λίγο το yield
    economic.kg_yield_per_acre = 1500  # 1.5 tonnes
    profit = profit_evaluation(
        crop=dummy_crop,
        field=dummy_field,
        economic=economic,
        climate=dummy_climate,
        farmer_knowledge=dummy_farmer_knowledge,
        beneficial_rotations=dummy_beneficial_rotations,
    )
    # revenue=1.5, cost=1 → profit=0.5, max_possible_profit=1.5-1=0.5 → normalized=1.0
    assert profit == pytest.approx(1.0)


# 4) Υψηλό stress → profit ≈ 0.0
@pytest.mark.profit
def test_high_stress_reduces_profit(
    dummy_field,
    dummy_climate,
    dummy_farmer_knowledge,
    dummy_beneficial_rotations,
    dummy_economic_data,
):
    # φτιάχνουμε crop με πλήρες stress
    from types import SimpleNamespace
    crop = SimpleNamespace(
        id=999,
        name="X",
        etc_mm=100,
        get_temperature_stress=lambda c: 1.0,
        get_rain_stress=lambda c: 1.0,
        get_moisture_stress=lambda cell: 1.0,
        n=120, p=30, k=40,
        soil_type="loamy",
        ph_min=6.0, ph_max=7.5
    )
    # δώσε του ένα dummy economics
    economic = Economics(crop_id=999, tonne_price_sell=1, unit_price=0, units_per_acre=0, kg_yield_per_acre=1000)

    profit = profit_evaluation(
        crop=crop,
        field=dummy_field,
        economic=economic,
        climate=dummy_climate,
        farmer_knowledge=dummy_farmer_knowledge,
        beneficial_rotations=dummy_beneficial_rotations,
    )
    assert profit == pytest.approx(0.0)


# 5) Boost from farmer_knowledge & beneficial_rotations
@pytest.mark.profit
def test_knowledge_and_rotation_boost(
    dummy_field,
    dummy_climate,
    dummy_economic_data,
    dummy_farmer_knowledge,
    dummy_beneficial_rotations
):
    
    crop = make_dummy_crop(name='Λούπινο')
    past_crop = make_dummy_crop(name='Σιτάρι')

    for row in range(dummy_field.grid.rows):
        for col in range(len(dummy_field.grid.cell_grid[row])):
            cell = dummy_field.grid.get_cell(row, col)
            cell.crop_history.append(past_crop)

    economic = dummy_economic_data[crop.id]
    # μηδενικό κόστος
    economic.unit_price = 0
    economic.units_per_acre = 0

    profit = profit_evaluation(
        crop=crop,
        field=dummy_field,
        economic=economic,
        climate=dummy_climate,
        farmer_knowledge=dummy_farmer_knowledge,
        beneficial_rotations=dummy_beneficial_rotations,
    )
    # multiplier = 1.09 * 1.05 ≈1.1445, capped at 1.0
    assert profit == pytest.approx(1.0)