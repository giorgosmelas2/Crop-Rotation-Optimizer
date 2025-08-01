import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.ml.optimization.run_optimizer import optimize_rotation_plan
from demo_data import (
    random_dummy_crops,
    dummy_pest_manager,
    dummy_pest_agents,
    dummy_past_pest_agents,
    random_dummy_field,
    random_dummy_climate,
    random_dummy_farmer_knowledge,
    random_dummy_beneficial_rotations,
    dummy_economic_data,
    random_dummy_missing_machinery,
    dummy_crops_required_machinery,
    random_dummy_past_crops,
    random_dummy_years,
)
from visualization.plots import all_plots   

def main():
    selected_crops = random_dummy_crops()
    print(f"Selected crops length: {len(selected_crops)}")
    past_crops = random_dummy_past_crops()
    print(f"Past crops length: {len(past_crops)}")

    dummy_pests =  dummy_pest_agents(selected_crops)
    print(f"Dummy pests length: {len(dummy_pests)}")

    dummy_past_pests = dummy_past_pest_agents(past_crops)
    print(f"Dummy past pests length: {len(dummy_past_pests)}")
    pest_manager = dummy_pest_manager(dummy_pests, dummy_past_pests)

    field = random_dummy_field()
    climate = random_dummy_climate()
    farmer_knowledge = random_dummy_farmer_knowledge()
    beneficial_rotations = random_dummy_beneficial_rotations()
    economic_data = dummy_economic_data()
    missing_machinery = random_dummy_missing_machinery()
    req_machinery = dummy_crops_required_machinery()
    years = random_dummy_years()

    best_individual, best_score, gens_best_fitness, gens_avg_fitness, gens_variance, gens_worst_fitness,= optimize_rotation_plan(
            selected_crops=selected_crops,
            pest_manager=pest_manager,
            field=field,
            climate=climate,
            farmer_knowledge=farmer_knowledge,
            beneficial_rotations=beneficial_rotations,
            economic_data=economic_data,
            missing_machinery=missing_machinery,
            crops_required_machinery=req_machinery,
            past_crops=past_crops,
            years=years,
            algorithm="deap",
        )

    print(f"\n🌾 Best individual (DEAP): {best_individual}\n⭐ Best score: {best_score:.3f}\n")
    all_plots(
        gens_best_fitness=gens_best_fitness,
        gens_avg_fitness=gens_avg_fitness,
        gens_variance=gens_variance,
        gens_worst_fitness=gens_worst_fitness,
    )

if __name__ == "__main__":
    main()
