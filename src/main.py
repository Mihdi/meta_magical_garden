from games.snake.snake_instructions import conditionally_jumps_to_position_if_next_is_0, load_state_at_position, submit_instruction_up, submit_instruction_right, submit_instruction_down, submit_instruction_left
from games.snake.snake_game_engine import snake_iteration
from utils.grid_utils import convert_2d_position_to_1d
from utils.print_utils import debug_post_iteration_callback
from engine.engine import perform_n_iterations

def main():
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


	grid_column_length = 10
	grid_row_length = 10

	n = 100

	game_iterate=snake_iteration
	agents=[
		[
			# apply same principle as the following pseudo assembly:
			# UP:
			# 	LOAD STATE UP TO NEXT DATA
			# 	IF 0 GOTO RIGHT 
			# 	UP
			# 	GOTO UP
			# RIGHT:
			# 	LOAD STATE RIGHT TO NEXT DATA
			# 	IF 0 GOTO DOWN
			# 	RIGHT
			# 	GOTO RIGHT
			# DOWN:
			# 	LOAD STATE DOWN TO NEXT DATA
			# 	IF 0 GOTO LEFT 
			# 	DOWN
			# 	GOTO DOWN
			# LEFT:
			# 	LOAD STATE LEFT TO NEXT DATA
			# 	IF 0 GOTO UP 
			# 	LEFT
			# 	GOTO LEFT
			ord('L'), ord('↑'),  4, ord('J'), ord('-'), 10, ord('↑'), ord('J'), 0,  0,
			ord('L'), ord('→'), 14, ord('J'), ord('-'), 20, ord('→'), ord('J'), 0, 10,
			ord('L'), ord('↓'), 24, ord('J'), ord('-'), 30, ord('↓'), ord('J'), 0, 20,
			ord('L'), ord('←'), 34, ord('J'), ord('-'), 00, ord('←'), ord('J'), 0, 30
		]
	]


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

	post_iteration_callback = debug_post_iteration_callback

	perform_n_iterations(
		n=n,
		post_iteration_callback=post_iteration_callback,

		# immutable between iterations
		game_iterate=game_iterate,
		instruction_set=instruction_set,
		instruction_costs=instruction_costs,

		# mutable between iterations
		agents=agents,
		game_state=game_state,
		pointers=pointers,
		agents_freeze_values=agents_freeze_values
	)


if __name__ == '__main__':
	main()