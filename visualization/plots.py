import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def fitness_evolution_plot(gens_best_fitness):
    plt.figure(figsize=(10,6))
    plt.plot(gens_best_fitness, marker='o', linestyle='-')
    plt.title('Best Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True)
    plt.tight_layout
    # plt.show()

def avg_fitness_evolution_plot(gens_avg_fitness):
    plt.figure(figsize=(10,6))
    plt.plot(gens_avg_fitness, marker='o', linestyle='-')
    plt.title('Average Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness Score')
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    
def combined_fitness_plot(gens_best_fitness, gens_variance, gens_worst_fitness):
    generations = list(range(len(gens_best_fitness)))
    plt.figure(figsize=(10,6))
    plt.plot(generations, gens_best_fitness, marker='o', label='Best')
    plt.plot(generations, gens_variance,      marker='s', label='Avg')
    plt.plot(generations, gens_worst_fitness, marker='^', label='Worst')
    plt.title('Fitness Evolution (Best / Avg / Worst)')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    # plt.show()

def variance_plot(gens_variance):
    plt.figure(figsize=(10,6))
    plt.plot(gens_variance, marker='o', linestyle='-')
    plt.title('Fitness Variance per Generation')
    plt.xlabel('Generation')
    plt.ylabel('Variance')
    plt.grid(True)
    plt.tight_layout()
    # plt.show()

def worst_fitness_evolution_plot(gens_worst_fitness):
    plt.figure(figsize=(10,6))
    plt.plot(gens_worst_fitness, marker='o', linestyle='-')
    plt.title('Worst Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Worst Fitness Score')
    plt.grid(True)
    plt.tight_layout()

def improvement_rate_plot(gens_best_fitness):
    improvements = [
        gens_best_fitness[i] - gens_best_fitness[i-1]
        for i in range(1, len(gens_best_fitness))
    ]
    plt.figure(figsize=(10,6))
    plt.plot(range(1, len(gens_best_fitness)), improvements, marker='o', linestyle='-')
    plt.axhline(0, linestyle='--')
    plt.title('Improvement Rate of Best Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Δ Best Fitness')
    plt.grid(True)
    plt.tight_layout()
  

def all_plots(gens_best_fitness, gens_avg_fitness, gens_variance, gens_worst_fitness):
    combined_fitness_plot(gens_best_fitness, gens_avg_fitness, gens_worst_fitness)
    variance_plot(gens_variance)
    improvement_rate_plot(gens_best_fitness)

    plt.show()
