import random
import hashlib
import numpy as np
from functools import partial
import multiprocessing
from multiprocessing import Manager, Value

from deap import base, creator, tools
from app.ml.core_models.crop import Crop
from app.ml.simulation_logic.simulation import simulate_crop_rotation

POPULATION_SIZE = 128
GENERATIONS = 500
MUTATION_RATE = 0.35
CROSSOVER_PROB = 0.8
MAX_NO_IMPROVEMENT = 70
# ELITE_SIZE = 10
STD_THRESHOLD = 0.01
PATIENCE_STD = 100
USE_SHARED_CACHE = False

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

def init_individual(crop_ids, rotation_length):
    return random.choices(crop_ids, k=rotation_length)

# --- Cache init ---
if USE_SHARED_CACHE:
    manager = Manager()
    evaluation_cache = manager.dict()
    hits = manager.Value('i', 0)
    misses = manager.Value('i', 0)
else:
    evaluation_cache = {}
    hits = Value('i', 0)
    misses = Value('i', 0)

def evaluate_individual(
        selected_crops,
        individual,  
        pest_manager, 
        field, 
        climate, 
        farmer_knowledge, 
        beneficial_rotations,
        economic_data, 
        missing_machinery, 
        crops_required_machinery, 
        past_crops, 
        years,
        evaluation_cache,
        hits,
        misses
    ) -> tuple[float]:

    key = hashlib.md5(np.array(individual, dtype=np.int32).tobytes()).digest()  

    if key in evaluation_cache:
        incr(hits)
        return evaluation_cache[key]
    else:
        incr(misses)

    individual_score = simulate_crop_rotation(
        selected_crops,
        field, 
        climate, 
        individual, 
        pest_manager, 
        farmer_knowledge, 
        beneficial_rotations,
        economic_data, 
        missing_machinery, 
        crops_required_machinery, 
        past_crops, 
        years
    )

    result = (individual_score,)
    evaluation_cache[key] = result
    return result


def mutate_individual(individual: list[int], crop_ids: list[int])  -> tuple[list[int]]:
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            replacement = random.choice([cid for cid in crop_ids if cid != individual[i]])
            individual[i] = replacement
    return (individual,)

def register_selection_method(method_name: str):
    if "select" in toolbox.__dict__:
        del toolbox.__dict__["select"]

    if method_name == "roulette":
        toolbox.register("select", tools.selRoulette)
    elif method_name == "best":
        toolbox.register("select", tools.selBest)
    elif method_name == "sustour":
        toolbox.register("select", tools.selStochasticUniversalSampling)
    elif method_name == "random":
        toolbox.register("select", tools.selRandom)
    elif method_name == "tournament":
        toolbox.register("select", tools.selTournament, tournsize=4)
    else:
        raise ValueError(f"Unknown selection method: {method_name}")

def run_ga_deap(
        selected_crops, 
        pest_manager,
        field, 
        climate, 
        farmer_knowledge, 
        beneficial_rotations,
        economic_data, 
        missing_machinery, 
        crops_required_machinery,
        past_crops, 
        years,
        selection_method="sustour",
        max_no_improvement=MAX_NO_IMPROVEMENT
    ):
    id_to_crop = {crop.id: crop for crop in selected_crops}
    crop_ids = [crop.id for crop in selected_crops]

    toolbox.register("individual", tools.initIterate, creator.Individual, partial(init_individual, crop_ids=crop_ids, rotation_length=2*years))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", mutate_individual, crop_ids=crop_ids) 
    register_selection_method(selection_method)

    def wrapped_evaluate(individual):
        return evaluate_individual(
            selected_crops,
            individual, 
            pest_manager, 
            field, 
            climate, 
            farmer_knowledge,
            beneficial_rotations, 
            economic_data, 
            missing_machinery, 
            crops_required_machinery, 
            past_crops, 
            years,
            evaluation_cache,
            hits,
            misses
        )

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    print(f"Processors: {multiprocessing.cpu_count()}")
    toolbox.register("map", lambda f, data: pool.map(f, data, chunksize=50))
    toolbox.register("evaluate", wrapped_evaluate)

    pop = toolbox.population(n=POPULATION_SIZE)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("max", np.max)
    stats.register("min", np.min)
    stats.register("var", np.var)
    logbook = tools.Logbook()
    logbook.header = ["gen", "avg", "min", "max", "var", "std", "best"]

    # Prepare print format
    header_fmt = "{:<4} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}"
    line_fmt = "{:<4d} {:<8.3f} {:<8.3f} {:<8.3f} {:<8.3f} {:<8.3f} {:<8.3f}"
    print(header_fmt.format("Gen", "Avg", "Max", "Min", "Var", "Std", "GlobBest"))

    # Evaluate initial population
    invalid = [ind for ind in pop if not ind.fitness.valid]
    for ind, fit in zip(invalid, map(toolbox.evaluate, invalid)):
        ind.fitness.values = fit
    hof.update(pop)
    record = stats.compile(pop)
    logbook.record(gen=0, **record)
    std_val = np.sqrt(record['var'])
    print(line_fmt.format(0, record['avg'], record['max'], record['min'], record['var'], std_val, hof[0].fitness.values[0]))

    # Early stopping variables
    best_score = record['max']
    no_improve = 0
    low_std_count = 0

    # Evolutionary loop
    for gen in range(1, GENERATIONS + 1):
        # Compute dynamic mutation rate
        mut_rate = MUTATION_RATE * (1 - gen / GENERATIONS)

        # Selection
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # Crossover
        for c1, c2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CROSSOVER_PROB:
                toolbox.mate(c1, c2)
                del c1.fitness.values, c2.fitness.values

        # Mutation with dynamic rate
        for mutant in offspring:
            for i in range(len(mutant)):
                if random.random() < mut_rate:
                    mutant[i] = random.choice([cid for cid in crop_ids if cid != mutant[i]])
            del mutant.fitness.values

        # Evaluate
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        for ind, fit in zip(invalid, map(toolbox.evaluate, invalid)):
            ind.fitness.values = fit

        

        # Update population and Hall of Fame
        # pop[:] = offspring
        # μ+λ
        pop[:] = tools.selBest(pop + offspring, POPULATION_SIZE)

        # μ,λ
        # pop[:] = tools.selBest(offspring, POPULATION_SIZE)
        hof.update(pop)

        record = stats.compile(pop)
        logbook.record(gen=gen, **record)
        std_val = np.sqrt(record['var'])
        print(line_fmt.format(gen, record['avg'], record['max'], record['min'], record['var'], std_val, hof[0].fitness.values[0]))

        #Early stopping check
        curr_best = record['max']
        if curr_best > best_score:
            best_score = curr_best
            no_improve = 0
        else:
            no_improve += 1
            if no_improve >= max_no_improvement:
                print(f"Stopping early at generation {gen} (no improvement for {max_no_improvement} gens).")
                break
        
        if std_val < STD_THRESHOLD:
            low_std_count += 1
        else:
            low_std_count = 0

        if low_std_count >= PATIENCE_STD:
            print(f"Stopping early at generation {gen} due to low std (< {STD_THRESHOLD}) for {PATIENCE_STD} generations.")
            break

    # Prepare results
    best_ids = list(hof[0])
    best_names = get_names_from_ids(best_ids, id_to_crop)
    best_fitness = [entry["max"] for entry in logbook]
    avg_fitness = [entry["avg"] for entry in logbook]
    worst_fitness = [entry["min"] for entry in logbook]
    variance = [entry["var"] for entry in logbook]
    best_score = hof[0].fitness.values[0]

    pool.close()
    pool.join()

    print(f"Cache hits: {hits.value}, misses: {misses.value}")
    return (
        best_names,
        best_score,
        best_fitness,
        avg_fitness,
        worst_fitness,
        variance,
    )


# Helper function to get crop name from ids
def get_names_from_ids(best: list[int], id_to_crop: dict[int, Crop]) -> list[Crop]:
    return [id_to_crop[cid].name for cid in best]

def incr(counter):
    try:
        with counter.get_lock():
            counter.value += 1
    except AttributeError:
        try:
            counter.value += 1
        except AttributeError:
            counter.set(counter.get() + 1)