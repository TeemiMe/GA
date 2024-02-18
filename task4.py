import random
import matplotlib.pyplot as plt

# Define problem parameters
items = [("item1", 10, 5), ("item2", 8, 4), ("item3", 15, 7), ("item4", 5, 3)]  # (name, value, weight)
knapsack_capacity = 15
population_size = 100
mutation_rate = 0.02
elite_percentage = 0.1
max_generations = 1000

# Generate initial population
def generate_individual():
    return [random.randint(0, 1) for _ in range(len(items))]

def initial_population():
    return [generate_individual() for _ in range(population_size)]

# Calculate fitness of an individual
def calculate_fitness(individual):
    total_value = 0
    total_weight = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            total_value += items[i][1]
            total_weight += items[i][2]
    if total_weight > knapsack_capacity:
        return 0  # Penalize solutions exceeding capacity
    else:
        return total_value

# Selection: Roulette wheel selection
def selection(population):
    fitness_sum = sum(calculate_fitness(individual) for individual in population)
    probabilities = [calculate_fitness(individual) / fitness_sum for individual in population]
    return random.choices(population, probabilities, k=2)

# Crossover: Uniform crossover
def crossover(parent1, parent2):
    child1 = []
    child2 = []
    for gene1, gene2 in zip(parent1, parent2):
        if random.random() < 0.5:
            child1.append(gene1)
            child2.append(gene2)
        else:
            child1.append(gene2)
            child2.append(gene1)
    return child1, child2

# Mutation
def mutate(individual):
    mutated_individual = []
    for gene in individual:
        if random.random() < mutation_rate:
            mutated_individual.append(1 - gene)  # Flip the bit
        else:
            mutated_individual.append(gene)
    return mutated_individual

# Genetic algorithm
def genetic_algorithm():
    population = initial_population()
    generation = 0
    best_fit_chromosomes = []
    while generation < max_generations:
        population = sorted(population, key=calculate_fitness, reverse=True)
        best_fit = population[0]
        best_fit_chromosomes.append(calculate_fitness(best_fit))
        if calculate_fitness(best_fit) == 0:  # No feasible solution found
            break
        next_generation = [best_fit]
        elite_count = int(population_size * elite_percentage)
        next_generation.extend([mutate(child) for parent1, parent2 in [selection(population) for _ in range(population_size - elite_count)] for child in crossover(parent1, parent2)])
        population = next_generation
        generation += 1
    return population[0], best_fit_chromosomes

# Run genetic algorithm
best_solution, best_fit_chromosomes = genetic_algorithm()
print("Best Solution:", best_solution)

# Plot performance graph
plt.plot(range(1, len(best_fit_chromosomes) + 1), best_fit_chromosomes)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Performance of Genetic Algorithm')
plt.show()