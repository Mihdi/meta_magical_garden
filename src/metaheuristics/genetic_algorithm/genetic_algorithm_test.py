from random import random, randint
from typing import Callable, List
from statistics import mean 

from .genetic_algorithm import apply_genetic_algorithm_iteration, PopulationReplacementStrategy
import matplotlib.pyplot as plt

def generate_polynomial_fitness(
	target: float,
	x: float,
) -> Callable[(List[float]), float]:
	def polynomial_fitness(agent: List[float], target: float, x: float) -> float:
		y = sum([agent[i] * (x ** i) for i in range(len(agent))])
		return -1 * abs(y - target)
	return lambda agent, target=target, x=x: polynomial_fitness(agent=agent, target=target, x=x)

def bigger_is_better(x):
	return sum(x)

def no_repeat_int_random_generator(length: int, min_val: int, max_val: int):
	assert (max_val - min_val) >= (length - 1), f"got a range of {max_val - min_val} values for a length of {length -1}."
	all_values = list(range(min_val, max_val))
	all_values.sort(key=lambda _: random())

	return all_values[:length]

def crossover(
	parents: List[List[float]]
) -> List[List[float]]:
	split_point = randint(0, len(parents[0])-1)
	return [
		parents[0][:split_point] + parents[1][split_point:],
		parents[1][:split_point] + parents[0][split_point:],
	]

def graph_results(results):
	mean_fitnesses = [r[0] for r in results]
	max_fitnesses = [r[1] for r in results]
	x = list(range(len(results)))
	y_mean = mean_fitnesses
	y_max = max_fitnesses
	plt.plot(x, y_mean, label = "mean")
	plt.plot(x, y_max, label = "max")
	plt.legend()
	plt.show()

def test():
	population_size = 100
	generate_agent = lambda: random() * 100 - 50
	population = [[generate_agent() for _ in range(randint(1, 10))] for _ in range(population_size)]
	compute_fitness_for_individual = generate_polynomial_fitness(target = 420, x=69) # bigger_is_better(x) 
	compute_fitness = lambda pop: [compute_fitness_for_individual(p) for p in pop]
	selection_rate = 0.95
	population_replacement_strategy = PopulationReplacementStrategy.ELITIST
	random_generator = lambda n: [random() for _ in range(n)]
	nb_parents_for_crossover = 2
	mutation_rate = 0.05
	mutate = lambda agent: [generate_agent() if i == randint(0, len(agent)-1) else agent[i] for i in range(len(agent))]

	results = []
	for i in range(100*1000):
		population = apply_genetic_algorithm_iteration(
			population=population,
			compute_fitness=compute_fitness,
			selection_rate=selection_rate,
			population_replacement_strategy=population_replacement_strategy,
			random_generator=random_generator,
			no_repeat_int_random_generator=no_repeat_int_random_generator,
			crossover=crossover,
			nb_parents_for_crossover=nb_parents_for_crossover,
			mutation_rate=mutation_rate,
			mutate=mutate,
		)

		if i % 1000 == 0:
			fitness = compute_fitness(population)
			mean_fitness = mean(fitness)
			max_fitness = max(fitness)
			results.append((mean_fitness, max_fitness))
			print(f"max_fitness: <{max_fitness}>\tmean_fitness:{mean_fitness}")

	max_fitnesses = [r[1] for r in results]
	assert max_fitnesses[-1] >= max_fitnesses[0]
	graph_results(results)
