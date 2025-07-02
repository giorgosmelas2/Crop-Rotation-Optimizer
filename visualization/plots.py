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

def prepare_pest_frames(pest_tracking: dict):
    cell_coords = list(pest_tracking.keys())
    month_keys = list(next(iter(pest_tracking.values())).keys())

    max_row = max(coord[0] for coord in cell_coords) + 1
    max_col = max(coord[1] for coord in cell_coords) + 1

    frames = []
    for month in month_keys:
        grid = np.zeros((max_row, max_col))
        for (row, col), data in pest_tracking.items():
            grid[row, col] = data.get(month, 0.0)
        frames.append(grid)
    
    return frames, month_keys

def animate_pest_pressure(frames, month_keys, save_path: str = None):
    fig, ax = plt.subplots()
    im = ax.imshow(frames[0], cmap="Reds")

    def update(frame_index):
        im.set_array(frames[frame_index])
        ax.set_title(f"Pest Pressure - {month_keys[frame_index]}")
        return [im]
    
    ani = animation.FuncAnimation(
        fig, update, frames=len(frames), interval=500, blit=True, repeat=False
    )

    plt.colorbar(im, ax=ax)
    plt.tight_layout()

    if save_path:
        ani.save(save_path, writer="pillow" if save_path.endswith('.gif') else 'ffmpeg', fps=2)
    else:
        plt.show()

