import pytest

from app.ml.optimization.run_optimizer import optimize_rotation_plan
from visualization.plots import all_plots
from tests.conftest import make_dummy_pest_agent

@pytest.mark.ga_custom
def run_rotation_simulation(
    dummy_crops,
    dummy_pest_manager,
    random_dummy_field,
    random_dummy_climate,
    random_dummy_farmer_knowledge,
    random_dummy_beneficial_rotations,
    dummy_economic_data,
    random_dummy_missing_machinery,
    dummy_crops_required_machinery,
    random_dummy_past_crops,
    random_dummy_years,
):
    best_names, score, gens_best_fitness, avg_fitness, variance_per_gen, pest_tracking = optimize_rotation_plan(
        crops=dummy_crops,
        pest_manager=dummy_pest_manager,
        field=random_dummy_field,
        climate=random_dummy_climate,
        farmer_knowledge=random_dummy_farmer_knowledge,
        beneficial_rotations=random_dummy_beneficial_rotations,
        economic_data=dummy_economic_data,
        missing_machinery=random_dummy_missing_machinery,
        crops_required_machinery=dummy_crops_required_machinery,
        past_crops=random_dummy_past_crops,
        years=random_dummy_years,
        algorithm="custom",
    )

    print(f"\n🌾 Best rotation: {best_names}\n⭐ Best score: {score:.3f}\n")
    all_plots(gens_best_fitness, avg_fitness, variance_per_gen, pest_tracking)

# @pytest.mark.ga_deap
# def test_optimize_rotation_deap(
#     dummy_field,
#     dummy_climate,
#     make_dummy_crop,
#     dummy_farmer_knowledge,
#     dummy_beneficial_rotations,
#     dummy_economic_data,
#     dummy_missing_machinery,
#     dummy_crops_required_machinery,
#     dummy_past_crops,
#     dummy_years,
#     dummy_pest_manager,
# ):
#     # Ξαναχτίζουμε crops
#     crops = [
#         make_dummy_crop(id=1, name="Σιτάρι", sow_month=1, harvest_month=2, pest="TestPest"),
#         make_dummy_crop(id=2, name="Λούπινο", sow_month=3, harvest_month=4, pest="TestPest"),
#         make_dummy_crop(id=3, name="Ρύζι",   sow_month=5, harvest_month=6, pest="TestPest"),
#     ]

#     # Καλούμε με τον DEAP αλγόριθμο
#     best_names, score, gens_best, avg_fitness, var_per_gen, pest_tracking = optimize_rotation_plan(
#         crops=crops,
#         pest_manager=dummy_pest_manager,
#         field=dummy_field,
#         climate=dummy_climate,
#         farmer_knowledge=dummy_farmer_knowledge,
#         beneficial_rotations=dummy_beneficial_rotations,
#         economic_data=dummy_economic_data,
#         missing_machinery=dummy_missing_machinery,
#         crops_required_machinery=dummy_crops_required_machinery,
#         past_crops=dummy_past_crops,
#         years=dummy_years,
#         algorithm="deap",
#     )

#     # Ίδιοι έλεγχοι τύπων όπως παραπάνω
#     assert isinstance(best_names, list)
#     assert isinstance(score, float)
#     assert 0.0 <= score <= 1.0
#     assert isinstance(gens_best, list)
#     assert isinstance(avg_fitness, list)
#     assert isinstance(var_per_gen, list)
#     assert isinstance(pest_tracking, dict)

# def test_optimize_invalid_algorithm(
#     dummy_field,
#     dummy_climate,
#     make_dummy_crop,
#     dummy_farmer_knowledge,
#     dummy_beneficial_rotations,
#     dummy_economic_data,
#     dummy_missing_machinery,
#     dummy_crops_required_machinery,
#     dummy_past_crops,
#     dummy_years,
#     dummy_pest_manager,
# ):
#     with pytest.raises(ValueError):
#         optimize_rotation_plan(
#             crops=[make_dummy_crop()],
#             pest_manager=dummy_pest_manager,
#             field=dummy_field,
#             climate=dummy_climate,
#             farmer_knowledge=dummy_farmer_knowledge,
#             beneficial_rotations=dummy_beneficial_rotations,
#             economic_data=dummy_economic_data,
#             missing_machinery=dummy_missing_machinery,
#             crops_required_machinery=dummy_crops_required_machinery,
#             past_crops=dummy_past_crops,
#             years=dummy_years,
#             algorithm="unknown",
#         )
