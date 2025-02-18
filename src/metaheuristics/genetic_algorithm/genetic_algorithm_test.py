from random import random, randint
from typing import Callable, List

from .genetic_algorithm import apply_genetic_algorithm_iteration, PopulationReplacementStrategy

def generate_polynomial_fitness(
	target: float,
	x: float,
) -> Callable[(List[float]), float]:
	def polynomial_fitness(agent: List[float], target: float, x: float) -> float:
		y = sum([agent[i] * (x ** i) for i in range(len(agent))])
		return -1 * abs(y - target)
	return lambda agent, target=target, x=x: polynomial_fitness(agent=agent, target=target, x=x)

def no_repeat_int_random_generator(length: int, min_val: int, max_val: int):
	assert (max_val - min_val) >= (length - 1), f"got a range of {max_val - min_val} values for a length of {length -1}."
	all_values = list(range(min_val, max_val))
	all_values.sort(key=lambda _: random())

	return all_values[:length]

def crossover(
	parents: List[List[float]]
) -> List[List[float]]:
	split_point = randint(0, len(parents[0]))
	return [
		parents[0][:split_point] + parents[1][split_point:],
		parents[1][:split_point] + parents[0][split_point:],
	]


def test():
	population_size = 100
	generate_agent = lambda: random() * 100 - 50
	population = [[generate_agent() for _ in range(randint(1, 10))] for _ in range(population_size)]
	compute_fitness_for_individual = generate_polynomial_fitness(target = 420, x=69)
	compute_fitness = lambda pop: [compute_fitness_for_individual(p) for p in pop]
	selection_rate = 0.95
	population_replacement_strategy = PopulationReplacementStrategy.ELITIST
	random_generator = lambda n: [random() for _ in range(n)]
	nb_parents_for_crossover = 2
	mutation_rate = 0.05
	mutate = lambda agent: [generate_agent() if i == randint(0, len(agent)) else agent[i] for i in range(len(agent))]

	for i in range(1000):
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

		if i % 10 == 0:
			fitness = min(compute_fitness(population))
			print(f"fitness at #{i} is <{fitness}>")

	assert True