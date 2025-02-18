from typing import Callable, List, Tuple
from enum import Enum

def elitist_replacement(
	sorted_population: List[any]
):
	""" replace the n eliminated unfit agents by the n best fit """
	sorted_population = [
		sorted_population[i] if sorted_population[i] is not None 
		else sorted_population[len(sorted_population) - i - 1]
		for i in range(len(sorted_population))
	]
	return sorted_population


def winner_takes_it_all_replacement(
	sorted_population: List[any]
):
	""" replace all the unfit agents with the best fit """
	if len(sorted_population) == 0:
		return []

	sorted_population = [
		sorted_population[i] if sorted_population[i] is not None
		else sorted_population[0]
	]

	return sorted_population


class PopulationReplacementStrategy(object):
	"""PopulationReplacementStrategy lists the strategies allowed to replace unfit agents"""
	ELITIST = elitist_replacement,
	WINNER_TAKES_IT_ALL = winner_takes_it_all_replacement,


def apply_genetic_algorithm_iteration(
	population: List[any],
	compute_fitness: Callable[(List[any]), List[float]],
	selection_rate: float,
	population_replacement_strategy: PopulationReplacementStrategy,
	random_generator: Callable[(int), List[float]], # input = len(output)
	no_repeat_int_random_generator: Callable[(int, int, int), List[int]], # first is len(output), second is min included, third is max excluded
	crossover: Callable[(List[any]), List[any]], # takes n agents and returns n agents
	nb_parents_for_crossover: int,
	# nb_crossovers: int, todo: out of laziness, for now, only one crossover per iteration. Sorry. Feel free to implement more.
	mutation_rate: float,
	mutate: Callable[(any), any],
) -> List[any]:
	# initialization
	# fitness
	fitness = compute_fitness(population)
	sorted_population_by_fitness = zip(
		population,
		fitness
	).sort(
		key=lambda pf: pf[1], # order by fitness
		reverse=True # make it in decreasing order
	)

	# selection
	nb_survivors = int(len(population) * selection_rate)
	population = [
		sorted_population_by_fitness[i][0] if i < nb_survivors else None
		for i in range(len(population))
	]
	population = population_replacement_strategy.value(population)

	# crossover
	parents = no_repeat_int_random_generator(nb_parents_for_crossover, 0, len(population))
	children = crossover([population[i] for i in parents])
	
	for i, parent_index in enumerate(parents):
		population[parent_index] = children[i]

	# mutation
	is_mutant = [roll < mutation_rate for roll in random_generator(len(population))]
	population = [mutate(population[i]) if is_mutant[i] else  population[i] for i in range(len(population))]

	return population
