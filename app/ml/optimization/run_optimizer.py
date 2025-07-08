def optimize_rotation_plan(
    crops,
    pest_manager,
    field,
    climate,
    farmer_knowledge,
    economic_data,
    missing_machinery,
    crops_required_machinery,
    past_crops,
    years,
    algorithm="custom"
):
    if algorithm == "deap":
        from app.ml.optimization.genetic_deap import run_ga_deap
        best, score, gens_best_fitness, avg_fitness, variance_per_gen, pest_tracking = run_ga_deap(
            crops, 
            pest_manager,
            field, 
            climate,
            farmer_knowledge, 
            economic_data,
            missing_machinery,
            crops_required_machinery,
            past_crops,
            years
        )
    elif algorithm == "custom":
        from app.ml.optimization.genetic_custom import run_ga_custom
        best, score, gens_best_fitness, avg_fitness, variance_per_gen, pest_tracking = run_ga_custom(
            crops, 
            pest_manager,
            field, 
            climate,
            farmer_knowledge, 
            economic_data,
            missing_machinery, 
            crops_required_machinery,
            past_crops,
            years
        )
    else:
        raise ValueError("Unsupported algorithm type. Use 'deap' or 'custom'.")

    return [crop.name for crop in best], score, gens_best_fitness, avg_fitness, variance_per_gen, pest_tracking

