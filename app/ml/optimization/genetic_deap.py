import random
from deap import base, creator, tools, algorithms
from app.ml.core_models.crop import Crop
from app.ml.simulation_logic.simulation import simulate_crop_rotation

ROTATION_LENGTH = 4 
POPULATION_SIZE = 20
MUTATION_RATE = 0.2
CROSSOVER_PROB = 0.7
GENERATIONS = 30

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox

def init_individual(crops, rotation_length):
    return random.choices(crops, k=rotation_length)

toolbox.register("individual", tools.initIterate, creator.Individual, init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate_individual(individual, *args):
    # Here you pass whatever extra args your simulation needs
    individual_score = simulate_crop_rotation(*args, crops=individual)
    return (individual_score,)  # tuple for DEAP compatibility

def mutate_individual(individual: list[Crop], all_crops: list[Crop]):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            replacement = random.choice([c for c in all_crops if c.name != individual[i].name])
            individual[i] = replacement
    return (individual,)

toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mutate_individual, all_crops=None)  # to be set at runtime
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate_individual)  # wrapped at runtime

def run_ga_deap(
        crops, 
        field_state, 
        climate_df, 
        farmer_knowledge, 
        economic_data, 
        missing_machinery, 
        past_crops, 
        years
    ):
    toolbox.unregister("mutate")  # Reset in case
    toolbox.register("mutate", mutate_individual, all_crops=crops)

    def wrapped_evaluate(ind):
        return toolbox.evaluate(
            ind, field_state, climate_df, farmer_knowledge, economic_data, missing_machinery, years
        )

    toolbox.register("evaluate", wrapped_evaluate)

    pop = toolbox.population(n=POPULATION_SIZE)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda fits: sum(f[0] for f in fits) / len(fits))
    stats.register("max", lambda fits: max(f[0] for f in fits))

    pop, log = tools.eaSimple(
        pop, toolbox,
        cxpb=CROSSOVER_PROB, mutpb=MUTATION_RATE,
        ngen=GENERATIONS,
        stats=stats, halloffame=hof, verbose=True
    )

    best = hof[0]
    return best, best.fitness.values[0], log
