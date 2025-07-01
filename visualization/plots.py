import matplotlib.pyplot as plt

def fitness_evolution_plot(gens_best_fitness):
    plt.figure(figsize=(10,6))
    plt.plot(gens_best_fitness, marker='o', linestyle='-')
    plt.title('Best Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True)
    plt.tight_layout
    plt.show()

def avg_fitness_evolution_plot(avg_fitness):
    plt.figure(figsize=(10,6))
    plt.plot(avg_fitness, marker='o', linestyle='-')
    plt.title('Average Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness Score')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def combined_fitness_plot(gens_best_fitness, avg_fitness):
    generations = list(range(len(gens_best_fitness)))
    plt.figure(figsize=(10,6))
    plt.plot(generations, gens_best_fitness, marker='o', label='Best fitness')
    plt.plot(generations, avg_fitness, marker='s', label='Average fitness')
    plt.title('Fitness Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Score')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def variance_plot(variance_per_gen):
    plt.figure(figsize=(10,6))
    plt.plot(variance_per_gen, marker='o', linestyle='-')
    plt.title('Fitness Variance per Generation')
    plt.xlabel('Generation')
    plt.ylabel('Variance')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
