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
	verbose = False
) -> List[any]:
	# initialization
	# fitness
	fitness = compute_fitness(population)
	population_by_fitness = list(
		zip(
			population,
			fitness
		)
	)
	population_by_fitness.sort(
		key=lambda pf: pf[1], # order by fitness
		reverse=True # make it in decreasing order
	)

	# selection
	nb_survivors = int(len(population_by_fitness) * selection_rate)
	surviving_population = [
		population_by_fitness[i][0] if i < nb_survivors else None
		for i in range(len(population_by_fitness))
	]
	replaced_population = population_replacement_strategy[0](surviving_population)

	# crossover
	parents = no_repeat_int_random_generator(nb_parents_for_crossover, 0, len(replaced_population))
	children = crossover([replaced_population[i] for i in parents])
	
	post_crossover_pop = [p for p in replaced_population]
	for i, parent_index in enumerate(parents):
		post_crossover_pop[parent_index] = children[i]

	# mutation
	is_mutant = [roll < mutation_rate for roll in random_generator(len(post_crossover_pop))]
	out = [mutate(post_crossover_pop[i]) if is_mutant[i] else post_crossover_pop[i] for i in range(len(post_crossover_pop))]

	if verbose:
		print(f"population_by_fitness: {population_by_fitness}")
		print(f"surviving_population: {surviving_population}")
		print(f"replaced_population: {replaced_population}")
		print(f"post_crossover_pop: {post_crossover_pop}")
		print(f"out: {out}")

	return out
