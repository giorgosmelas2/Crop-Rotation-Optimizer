import os
from pathlib import Path
import pandas as pd
from time import time
from ga_experiments_runner import run_ga_deap

loops_for_each_experiment = 8
parameters = [
    # # === Baselines === 
    # {"selection_method": "tournament", "poplupation_size": 128, "elitism": 1, # ok
    #  "generations": 400, "mutation_rate": 0.15, "crossover_prob": 0.9,
    #  "max_no_improvement": 80, "std_threshold": 0.005, "patience_std": 70},

    # {"selection_method": "tournament", "poplupation_size": 128, "elitism": 2, #ok
    #  "generations": 400, "mutation_rate": 0.15, "crossover_prob": 0.9,
    #  "max_no_improvement": 80, "std_threshold": 0.005, "patience_std": 70},

    # # === High-exploration ===
    # {"selection_method": "sustour", "poplupation_size": 64, "elitism": 0, # ok
    #  "generations": 600, "mutation_rate": 0.25, "crossover_prob": 0.85,
    #  "max_no_improvement": 120, "std_threshold": 0.01, "patience_std": 100},

    # {"selection_method": "sustour", "poplupation_size": 128, "elitism": 1, # ok
    #  "generations": 500, "mutation_rate": 0.3, "crossover_prob": 0.90,
    #  "max_no_improvement": 120, "std_threshold": 0.01, "patience_std": 100},  

    # # === High-exploitation ===
    # {"selection_method": "tournament", "poplupation_size": 128, "elitism": 2, # ok
    #  "generations": 300, "mutation_rate": 0.1, "crossover_prob": 0.9,
    #  "max_no_improvement": 200, "std_threshold": 0.004, "patience_std": 50},

    # {"selection_method": "tournament", "poplupation_size": 256, "elitism": 2, #ok
    #  "generations": 300, "mutation_rate": 0.05, "crossover_prob": 0.9,
    #  "max_no_improvement": 60, "std_threshold": 0.004, "patience_std": 50},

    # # === No-elitism control (να δεις αν σφραγίζει πρόωρα ο GA) ===
    # {"selection_method": "tournament", "poplupation_size": 128, "elitism": 0, # ok
    #  "generations": 400, "mutation_rate": 0.15, "crossover_prob": 0.90,
    #  "max_no_improvement": 120, "std_threshold": 0.010, "patience_std": 100},

    # # exploration + exploitation
    # {"selection_method": "sustour", "poplupation_size": 160, "elitism": 2,
    #  "generations": 500, "mutation_rate": 0.18, "crossover_prob": 0.92,
    #  "max_no_improvement": 140, "std_threshold": 0.008, "patience_std": 90},

    # {"selection_method": "tournament", "poplupation_size": 160, "elitism": 2,
    # "generations": 450, "mutation_rate": 0.15, "crossover_prob": 0.92,
    # "max_no_improvement": 120, "std_threshold": 0.006, "patience_std": 80},


    # # 5) SUS+Tournament, μ+λ, “ψηλό” crossover για mixing
    # {"selection_method": "sustour", "poplupation_size": 128, "elitism": 2,
    # "generations": 480, "mutation_rate": 0.16, "crossover_prob": 0.95,
    # "max_no_improvement": 130, "std_threshold": 0.007, "patience_std": 90},

    # # 6) Roulette, μ+λ, ελαφρώς χαμηλότερο mutation για σταθερότητα
    # {"selection_method": "roulette", "poplupation_size": 160, "elitism": 2,
    #  "generations": 450, "mutation_rate": 0.13, "crossover_prob": 0.92,
    #  "max_no_improvement": 140, "std_threshold": 0.006, "patience_std": 90},

    # # 7) Tournament, μ+λ, μεγαλύτερο population για διατήρηση diversity
    # {"selection_method": "tournament", "poplupation_size": 192, "elitism": 2,
    # "generations": 420, "mutation_rate": 0.15, "crossover_prob": 0.90,
    # "max_no_improvement": 140, "std_threshold": 0.007, "patience_std": 100},

    # {"selection_method": "roulette", "poplupation_size": 192, "elitism": 1,
    # "generations": 500, "mutation_rate": 0.14, "crossover_prob": 0.93,
    # "max_no_improvement": 150, "std_threshold": 0.007, "patience_std": 100},

    #     # 4) Tournament, μ,λ, μικρότερο population για πιο “σφιχτή” εκμετάλλευση
    # {"selection_method": "tournament", "poplupation_size": 128, "elitism": 1,
    # "generations": 450, "mutation_rate": 0.12, "crossover_prob": 0.95,
    # "max_no_improvement": 120, "std_threshold": 0.006, "patience_std": 80},


    # # 8) SUS+Tournament, μ,λ, λίγο πιο “ψαγμένο” exploration με patience μεγαλύτερο
    # {"selection_method": "sustour", "poplupation_size": 144, "elitism": 1,
    # "generations": 520, "mutation_rate": 0.17, "crossover_prob": 0.93,
    # "max_no_improvement": 160, "std_threshold": 0.008, "patience_std": 110},

    # Config 7
    {"selection_method": "sustour", "poplupation_size": 160, "elitism": 2, "elite_size": 1,
    "generations": 700, "mutation_rate": 0.18, "crossover_prob": 0.88,
    "max_no_improvement": 140, "std_threshold": 0.008, "patience_std": 150},

    {"selection_method": "sustour", "poplupation_size": 160, "elitism": 2, "elite_size": 2,
    "generations": 600, "mutation_rate": 0.20, "crossover_prob": 0.88,
    "max_no_improvement": 140, "std_threshold": 0.008, "patience_std": 120},

    {"selection_method": "sustour", "poplupation_size": 160, "elitism": 2, "elite_size": 3,
    "generations": 500, "mutation_rate": 0.22, "crossover_prob": 0.91,
    "max_no_improvement": 140, "std_threshold": 0.008, "patience_std": 110},

    # Config 10
    {"selection_method": "roulette", "poplupation_size": 160, "elitism": 2, "elite_size": 1,
    "generations": 700, "mutation_rate": 0.13, "crossover_prob": 0.92,
    "max_no_improvement": 140, "std_threshold": 0.006, "patience_std": 90},

    {"selection_method": "roulette", "poplupation_size": 160, "elitism": 2, "elite_size": 2,
    "generations": 600, "mutation_rate": 0.16, "crossover_prob": 0.9,
    "max_no_improvement": 140, "std_threshold": 0.006, "patience_std": 90},

    {"selection_method": "roulette", "poplupation_size": 160, "elitism": 2, "elite_size": 3,
    "generations": 500, "mutation_rate": 0.2, "crossover_prob": 0.92,
    "max_no_improvement": 140, "std_threshold": 0.006, "patience_std": 90},

]

LOG_DIR = Path(r"C:\Users\giorg\Desktop\δυπλωματικη εργασια\κειμενο")
LOG_DIR.mkdir(parents=True, exist_ok=True) 
LOG_PATH = LOG_DIR / "phase_2_expirement_runs5.xlsx"
SHEET_NAME = "runs"

def append_run_to_excel(row_dict, excel_path=LOG_PATH, sheet_name=SHEET_NAME):
    df_new = pd.DataFrame([row_dict])
    if excel_path.exists():
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            try:
                existing = pd.read_excel(excel_path, sheet_name=sheet_name)
                startrow = len(existing) + 1  
            except ValueError:
                startrow = 0
            df_new.to_excel(writer, sheet_name=sheet_name, index=False, header=(startrow == 0), startrow=startrow)
    else:
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df_new.to_excel(writer, sheet_name=sheet_name, index=False)

def experiment_optimize_rotation_plan(
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
):
    for index, parameter in enumerate(parameters):
        print(f"Running parameters: {index + 1}")
        for i in range(loops_for_each_experiment):
            print(f"Loop {i + 1} for parameters: {index + 1}")
            # print(f"Loop {i + 1}")
            t0 = time()
            best_individual, best_score, gens_best_fitness, gens_avg_fitness, gens_variance, gens_worst_fitness, diversity_tail, has_diversity, earlystop_gens, earlystop_std, gen = run_ga_deap(
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
                parameter["selection_method"],
                parameter["max_no_improvement"],
                parameter["poplupation_size"],
                parameter["elitism"],
                parameter["generations"], 
                parameter["mutation_rate"], 
                parameter["crossover_prob"], 
                parameter["std_threshold"],
                parameter["patience_std"],
                parameter["elite_size"],
            )
            elapsed = time() - t0

            row = {
                "poplupation_size": parameter["poplupation_size"],
                "generations": parameter["generations"],
                "selection_method": parameter["selection_method"],
                "elistm": parameter["elitism"],
                "eilite_size": parameter["elite_size"],
                "mutation_rate": parameter["mutation_rate"],
                "crossover_prob": parameter["crossover_prob"],
                "max_no_improvement": parameter["max_no_improvement"],
                "std_threshold": parameter["std_threshold"],
                "patience_std": parameter["patience_std"],  
                "diversity_tail": diversity_tail,
                "has_diversity": has_diversity,
                "best_score": best_score,
                "best_individual": best_individual,
                "elapsed_time": elapsed,
                "earlystop_gens": earlystop_gens,
                "earlystop_std": earlystop_std, 
                "generation_stop": gen,
            }
            append_run_to_excel(row)
            # print(f"Loop {i + 1} done.")
    
        print(f"End parameters:{index + 1}")



