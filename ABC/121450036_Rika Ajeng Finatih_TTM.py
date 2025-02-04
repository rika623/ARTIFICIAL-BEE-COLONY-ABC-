import random
import numpy as np

# Set seed untuk reproduktibilitas
random.seed(42)
np.random.seed(42)

# Menentukan parameter awal
num_employed_bees = 25
num_onlooker_bees = 25
max_iterations = 36
limit = 25
problem_size = 20

# Menentukan fitness function (fungsi tujuan)
def fitness_function(x):
    return np.sum(x**2)

# Inisialisasi populasi awal
food_sources = np.random.uniform(10, 20, size=(num_employed_bees, problem_size))
fitness_values = np.array([fitness_function(food) for food in food_sources])
no_improvement_counters = np.zeros(num_employed_bees)

# Loop utama
for iteration in range(max_iterations):
    # Fase Employed bees (Lebah Pekerja)
    for i in range(num_employed_bees):
        # Pilih dimensi secara acak untuk diubah
        dimension = random.randint(0, problem_size - 1)
        
        # Menghasilkan solusi kandidat baru (mutant)
        mutant = np.copy(food_sources[i])
        mutant[dimension] += (random.random() - 0.5) * 2  # Modifikasi dengan memilih dimensi random
        
        # Evaluasi fitness mutant
        mutant_fitness = fitness_function(mutant)
        
        # Seleksi Greedy antara solusi saat ini dan mutannya
        if mutant_fitness < fitness_values[i]:
            food_sources[i] = mutant
            fitness_values[i] = mutant_fitness
            no_improvement_counters[i] = 0
        else:
            no_improvement_counters[i] += 1

    # Hitung probabilitas berdasarkan nilai fitness
    total_fitness = np.sum(fitness_values)
    if total_fitness == 0:
        probabilities = np.ones(num_employed_bees) / num_employed_bees
    else:
        probabilities = (1.0 / (1.0 + fitness_values)) / np.sum(1.0 / (1.0 + fitness_values))

    # Fase Onlooker bees (Lebah Pengamat)
    for j in range(num_onlooker_bees):
        # Pilih sumber makanan berdasarkan seleksi roda roulette
        selected_food_source = np.random.choice(num_employed_bees, p=probabilities)
        
        # Pilih dimensi secara acak untuk diubah
        dimension = random.randint(0, problem_size - 1)
        
        # Hasilkan solusi kandidat baru (mutant)
        mutant = np.copy(food_sources[selected_food_source])
        mutant[dimension] += (random.random() - 0.5) * 2  # Modifikasi dimensi yang dipilih secara acak
        
        # Evaluasi fitness mutant
        mutant_fitness = fitness_function(mutant)
        
        # Seleksi Greedy antara solusi terpilih dan mutannya
        if mutant_fitness < fitness_values[selected_food_source]:
            food_sources[selected_food_source] = mutant
            fitness_values[selected_food_source] = mutant_fitness
            no_improvement_counters[selected_food_source] = 0
        else:
            no_improvement_counters[selected_food_source] += 1

    # Fase Scout bees (Lebah Penjajah)
    for k in range(num_employed_bees):
        if no_improvement_counters[k] > limit:
            food_sources[k] = np.random.uniform(10, 20, size=problem_size)
            fitness_values[k] = fitness_function(food_sources[k])
            no_improvement_counters[k] = 0

    # Tampilkan solusi terbaik dalam setiap iterasi
    best_fitness = np.min(fitness_values)
    print(f"Iterasi ke-{iteration}, Best Fitness: {best_fitness}")

# Temukan solusi terbaik secara keseluruhan
overall_best_fitness = np.min(fitness_values)
overall_best_index = np.argmin(fitness_values)
overall_best_solution = food_sources[overall_best_index]
print("--- Hasil Optimisasi ---")
print(f"Fitness Terbaik: {overall_best_fitness}")
print(f"Solution Terbaik: {overall_best_solution}")
