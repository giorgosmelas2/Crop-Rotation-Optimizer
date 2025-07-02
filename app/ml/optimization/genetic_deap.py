import random
import numpy as np
from functools import partial

from deap import base, creator, tools, algorithms
from app.ml.core_models.crop import Crop
from app.ml.simulation_logic.simulation import simulate_crop_rotation

POPULATION_SIZE = 20
MUTATION_RATE = 0.2
CROSSOVER_PROB = 0.7
GENERATIONS = 10

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

def init_individual(crops, rotation_length):
    return random.choices(crops, k=rotation_length)

def evaluate_individual(
        individual,  
        pest_manager, 
        field_state, 
        climate_df, 
        farmer_knowledge, 
        economic_data, 
        missing_machinery, 
        crops_required_machinery, 
        past_crops, 
        years 
    ) -> tuple[float]:

    individual_score, pest_tracking = simulate_crop_rotation(
        field_state, 
        climate_df, 
        individual, 
        pest_manager, 
        farmer_knowledge, 
        economic_data, 
        missing_machinery, 
        crops_required_machinery, 
        past_crops, 
        years
    )

    individual.pest_tracking = pest_tracking

    return (individual_score,)  # tuple for DEAP compatibility

def mutate_individual(individual: list[Crop], all_crops: list[Crop])  -> tuple[list[Crop]]:
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            replacement = random.choice([c for c in all_crops if c.name != individual[i].name])
            individual[i] = replacement
    return (individual,)

def run_ga_deap(
        crops, 
        pest_manager,
        field_state, 
        climate_df, 
        farmer_knowledge, 
        economic_data, 
        missing_machinery, 
        crops_required_machinery,
        past_crops, 
        years
    ):

    toolbox.register("individual", tools.initIterate, creator.Individual, partial(init_individual, crops=crops, rotation_length=years))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", mutate_individual, all_crops=crops) 
    toolbox.register("select", tools.selTournament, tournsize=3)

    def wrapped_evaluate(individual):
        return evaluate_individual(
            individual, 
            pest_manager, 
            field_state, 
            climate_df, 
            farmer_knowledge, 
            economic_data, 
            missing_machinery, 
            crops_required_machinery, 
            past_crops, 
            years
        )

    toolbox.register("evaluate", wrapped_evaluate)

    population = toolbox.population(n=POPULATION_SIZE)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda fits: sum(f[0] for f in fits) / len(fits))
    stats.register("max", lambda fits: max(f[0] for f in fits))
    stats.register("var", lambda fits: np.var([f[0] for f in fits]))

    population, logbook = algorithms.eaSimple(
        population, 
        toolbox,
        cxpb=CROSSOVER_PROB,
        mutpb=MUTATION_RATE,
        ngen=GENERATIONS,
        stats=stats, 
        halloffame=hof, 
        verbose=True
    )

    gen_best_fitness = [entry['max'] for entry in logbook]
    avg_fitness = [entry['avg'] for entry in logbook]
    variance_per_gen = [entry['var'] for entry in logbook]

    best = hof[0]
    pest_tracking = getattr(best, "pest_tracking", None)

    return best, best.fitness.values[0], gen_best_fitness, avg_fitness, variance_per_gen, pest_tracking
