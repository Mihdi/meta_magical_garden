from random import random, randint
from typing import Callable, List
from statistics import mean 
import matplotlib.pyplot as plt

from metaheuristics.genetic_algorithm.genetic_algorithm import apply_genetic_algorithm_iteration, PopulationReplacementStrategy
from games.snake.snake_instructions import conditionally_jumps_to_position_if_next_is_0, load_state_at_position, submit_instruction_up, submit_instruction_right, submit_instruction_down, submit_instruction_left
from games.snake.snake_game_engine import snake_game_generator
from utils.grid_utils import convert_2d_position_to_1d
from utils.print_utils import debug_post_iteration_callback
from engine.engine import perform_n_iterations

def generate_random_position_every_nth(current_i: int, n: int, distribution_range: int):
	if current_i % n == 0:
		out = randint(0, distribution_range-1)
		print(f"randint gave {out}")
		return [out]
	return []

def no_repeat_int_random_generator(length: int, min_val: int, max_val: int):
	assert (max_val - min_val) >= (length - 1), f"got a range of {max_val - min_val} values for a length of {length -1}."
	all_values = list(range(min_val, max_val))
	all_values.sort(key=lambda _: random())

	return all_values[:length]

def crossover(
	parents: List[List[int]]
) -> List[List[int]]:
	split_point = randint(0, len(parents[0]))
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


def higher_order_snake_fitness(
	number_of_iterations,
	grid_column_length,
	grid_row_length,
	instruction_set,
	instruction_costs,
	instruction_ticks_per_game_ticks,
) -> Callable[[List[List[int]]], int]:
	def snake_fitness(
			number_of_iterations,
			agents,
			grid_column_length,
			grid_row_length,
			instruction_set,
			instruction_costs,
			instruction_ticks_per_game_ticks,
	) -> int:
		grid_size = grid_column_length * grid_row_length
		pointers = [0 for _ in agents]
		agents_freeze_values = [0 for _ in agents]

		game_state = dict()
		game_state['dead_agents'] = [False for _ in agents]
		game_state['grid'] = [0 for _ in range(grid_column_length * grid_row_length)]
		game_state['grid_column_length'] = grid_column_length
		game_state['grid_row_length'] = grid_row_length
		game_state['agent_positions'] = [
			convert_2d_position_to_1d(0, 0, grid_column_length)
		]
		game_state['previous_actions'] = [None for _ in agents]
		game_state['turn_count'] = 0
		game_state['food_positions'] = [False for _ in range(grid_size)]
		game_state['resources'] = [{"food": 0} for _ in agents]

		post_iteration_callback = lambda _: ... # do nothing

		game_iterate=snake_game_generator(
			lambda turn_index, grid_size=grid_size: generate_random_position_every_nth(turn_index, 10, grid_size)
		)

		perform_n_iterations(
			n=number_of_iterations,
			post_iteration_callback=post_iteration_callback,

			# immutable between iterations
			game_iterate=game_iterate,
			instruction_set=instruction_set,
			instruction_costs=instruction_costs,
			instruction_ticks_per_game_ticks=instruction_ticks_per_game_ticks,

			# mutable between iterations
			agents=agents,
			game_state=game_state,
			pointers=pointers,
			agents_freeze_values=agents_freeze_values
		)
	return lambda agents, number_of_iterations=number_of_iterations, grid_column_length=grid_column_length, grid_row_length=grid_row_length, instruction_set=instruction_set, instruction_costs=instruction_costs, instruction_ticks_per_game_ticks=instruction_ticks_per_game_ticks: snake_fitness(
			agents=agents,
			number_of_iterations=number_of_iterations,
			grid_column_length=grid_column_length,
			grid_row_length=grid_row_length,
			instruction_set=instruction_set,
			instruction_costs=instruction_costs,
			instruction_ticks_per_game_ticks=instruction_ticks_per_game_ticks
		)


def generate_random_instruction(instructions: List[int]) -> int:
	return instructions[randint(0, len(instructions)-1)]


def generate_snake_agent(
	agent_length: int,
	instructions: List[int],
):
	return [generate_random_instruction(instructions) for _ in range(agent_length)]

def crossover(
	parents: List[List[float]]
) -> List[List[float]]:
	split_point = randint(0, len(parents[0])-1)
	return [
		parents[0][:split_point] + parents[1][split_point:],
		parents[1][:split_point] + parents[0][split_point:],
	]

def test():
	instruction_set = dict()
	instruction_set[ord('J')] = conditionally_jumps_to_position_if_next_is_0
	instruction_set[ord('L')] = load_state_at_position 
	instruction_set[ord('↑')] = submit_instruction_up
	instruction_set[ord('→')] = submit_instruction_right
	instruction_set[ord('↓')] = submit_instruction_down
	instruction_set[ord('←')] = submit_instruction_left

	instruction_costs = dict()
	instruction_costs[ord('J')] = 1
	instruction_costs[ord('L')] = 1
	instruction_costs[ord('↑')] = 1
	instruction_costs[ord('→')] = 1
	instruction_costs[ord('↓')] = 1
	instruction_costs[ord('←')] = 1

	# primitive config parameters
	agent_length = 100
	grid_column_length = 10
	grid_row_length = 10
	mutation_rate = 0.1
	nb_parents_for_crossover = 2
	population_replacement_strategy = PopulationReplacementStrategy.ELITIST
	population_size = 1000
	selection_rate = 0.8
	nb_ga_iterations = 1000
	frequency_of_result_collection = 100
	number_of_snake_iterations = 100
	instruction_ticks_per_game_ticks = 100

	assert nb_parents_for_crossover == 2, "todo: sorry for now we only handle 2 parents for a crossover, feel free to implem it for more"

	# you better know what you're doing kind of config parameters
	random_generator = lambda n: [random() for _ in range(n)]
	no_repeat_int_random_generator = lambda l, mn, mx: no_repeat_int_random_generator(l, mn, mx)
	crossover = lambda p: crossover(p) 
	instruction_list = list(instruction_set.keys())
	mutate = lambda agent, instructions=instruction_list: [generate_random_instruction(instructions) if i == randint(0, len(agent)-1) else agent[i] for i in range(len(agent))]

	# initialization
	generate_agent = lambda agent_length=agent_length, instructions=instruction_list: generate_snake_agent(agent_length=agent_length, instructions=instructions)
	fitness = higher_order_snake_fitness(
		number_of_snake_iterations,
		grid_column_length,
		grid_row_length,
		instruction_set,
		instruction_costs,
		instruction_ticks_per_game_ticks
	)
	population = [generate_agent() for _ in range(population_size)]
	compute_fitness = lambda pop: fitness(pop)

	results = []
	for i in range(nb_ga_iterations):
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

		if i % frequency_of_result_collection == 0:
			fitness = compute_fitness(population)
			mean_fitness = mean(fitness)
			max_fitness = max(fitness)
			results.append((mean_fitness, max_fitness))
			print(f"max_fitness: <{max_fitness}>\tmean_fitness:{mean_fitness}")

	max_fitnesses = [r[1] for r in results]
	assert max_fitnesses[-1] >= max_fitnesses[0]
	graph_results(results)


def main():
	print("hi")
	test()


if __name__ == '__main__':
	main()