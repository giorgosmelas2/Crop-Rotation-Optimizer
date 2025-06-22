import random
from deap import base, creator, tools, algorithms
from app.ml.core_models.crop import Crop
from app.ml.simulation_logic.simulation import simulate_crop_rotation 


# --- Custom GA Functions ---
def initialize_population(crops: list[Crop], population_size, rotation_length) -> list[list[Crop]]:
    """
    Initializes the population with random crop rotations.
    
    Args:
        crops (List[Crop]): Available crop options.
        population_size (int): Number of individuals in the population.
        rotation_length (int): Number of crops in each rotation plan (i.e., years).
    
    Returns:
        List[List[Crop]]: A list of individuals, each being a list of Crop objects.
    """

    population = []

    for _ in range(population_size):
        individual = random.choice(crops, k=rotation_length*2)
        population.append(individual)

    return population

def crossover(parent1: list[Crop], parent2: list[Crop]) -> tuple[list[Crop], list[Crop]]:
    """
    Performs one-point crossover between two parents.

    Args:
        parent1 (List[Crop]): First parent.
        parent2 (List[Crop]): Second parent.

    Returns:
        Tuple[List[Crop], List[Crop]]: Two offspring.
    """

    rotation_length = len(parent1)
    cut_point = random.randint(1, rotation_length - 1)

    child1 = parent1[:cut_point] + parent2[cut_point:]
    child2 = parent2[:cut_point] + parent1[cut_point:]

    return child1, child2

def mutate(individual: list[Crop], all_crops: list[Crop], mutation_rate: float) -> list[Crop]:
    """
    Applies mutation to an individual (i.e., a list of crops) by randomly
    swapping elements based on the given mutation rate.

    Args:
        individual (list[str]): The individual (crop sequence) to mutate.
        mutation_rate (float): Probability of mutation for each gene (between 0.0 and 1.0).

    Returns:
        list[str]: The mutated individual.
    """
    mutated = individual.copy()

    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            possible_replacements = [crop for crop in all_crops if crop.name != mutated[i].name]
            if possible_replacements:
                mutated[i] = random.choice(possible_replacements)

    return mutated

def select_parents(population, fitness_scores, method="tournament", tournament_size=3):
    def tournament_selection():
        def select_one():
            candidates = random.sample(list(zip(population, fitness_scores)), tournament_size)
            return max(candidates, key=lambda x: x[1])[0]
        return select_one(), select_one()
    
    def roulette_selection():
        total_fitness = sum(fitness_scores)
        probs = [f / total_fitness for f in fitness_scores]
        return random.choices(population, weights=probs, k=2)
    
    def rank_selection(): 
        sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1])
        ranks = list(range(1, len(sorted_population)+1)) # rank 1 to N
        total_rank = sum(ranks)
        probs = [r / total_rank for r in ranks]
        individuals = [ind for ind, _ in sorted_population]
        return random.choices(individuals, weights=probs, k=2)
    
    def sus_selection():
        total_fitness = sum(fitness_scores)
        probs = [f / total_fitness for f in fitness_scores]
        pointers = []
        start = random.uniform(0, 1/2)
        step = 1/2
        for i in range(2):
            pointers.append((start + i*step) % 1)
 
        cumulative = 0
        parents = []
        idx = 0
        for p in probs:
            cumulative += p
            while idx < len(pointers) and cumulative >= pointers[idx]:
                parents.append(population[i])
                idx += 1
        return parents[:2]

    if method == "tournament":
        return tournament_selection()
    elif method == "roulette":
        return roulette_selection()
    elif method == "rank":
        return rank_selection()
    elif method == "sus":
        return sus_selection()
    else:
        raise ValueError(f"Unknown selection method: {method}")

def run_ga_custom(
        crops,
        field_state,
        climate_df,
        farmer_knowledge,
        economic_data,
        missing_machinery,
        past_crops,
        rotation_length,
        population_size=30,
        generations=25,
        crossover_rate=0.7,
        mutation_rate=0.2,
        selection_method="tournament"
):
    population = initialize_population(crops, population_size, rotation_length)
    
    fitness_scores = []
    for individual in population:
        individual_score = simulate_crop_rotation(field_state, climate_df, individual, farmer_knowledge, economic_data, missing_machinery, past_crops, rotation_length)
        fitness_scores.append(individual_score)

    best_individual = population[fitness_scores.index(max(fitness_scores))]
    best_score = max(fitness_scores)

    logbook = []

    # --- Generations ---
    for gen in range(generations):
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, fitness_scores, method=selection_method)

            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            # Mutation
            child1 = mutate(child1, crops, mutation_rate)
            child2 = mutate(child2, crops, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population[:population_size]
        fitness_scores = []
        for individual in population:
            individual_score = simulate_crop_rotation(field_state, climate_df, individual, farmer_knowledge, economic_data, missing_machinery, years)
            fitness_scores.append(individual_score) 
        
        gen_best_score = max(fitness_scores)
        gen_best = population[fitness_scores.index(gen_best_score)]
        if gen_best_score > best_score:
            best_score = gen_best_score
            best_individual = gen_best

        logbook.append({
            "generation": gen,
            "max_score": gen_best_score,
            "avg_score": sum(fitness_scores) / len(fitness_scores),
        })

    return best_individual, best_score, logbook



 