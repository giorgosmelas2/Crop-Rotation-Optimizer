import sys, os
# Προσθέτουμε το root folder στο path, για να βρίσκει το πακέτο 'app' και το tests.conftest
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.ml.optimization.run_optimizer import optimize_rotation_plan
from demo_data import (
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
)
from visualization.plots import all_plots   # ή από όπου έχεις την all_plots

def main():
    # Καλούμε τις fixtures σαν απλές συναρτήσεις για να πάρουμε τα δεδομένα
    crops = dummy_crops()
    pest_manager = dummy_pest_manager()
    field = random_dummy_field()
    climate = random_dummy_climate()
    farmer_knowledge = random_dummy_farmer_knowledge()
    beneficial_rotations = random_dummy_beneficial_rotations()
    economic_data = dummy_economic_data()
    missing_machinery = random_dummy_missing_machinery()
    req_machinery = dummy_crops_required_machinery()
    past_crops = random_dummy_past_crops()
    years = random_dummy_years()

    best_names, score, gens_best_fitness, avg_fitness, variance_per_gen = optimize_rotation_plan(
            crops=crops,
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
            algorithm="custom",
        )

    print(f"\n🌾 Best rotation: {best_names}\n⭐ Best score: {score:.3f}\n")
    all_plots(gens_best_fitness, avg_fitness, variance_per_gen)

if __name__ == "__main__":
    main()
