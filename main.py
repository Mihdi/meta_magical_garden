from typing import Callable, Dict, Optional, List, Tuple

# each tick, game takes vector of actions and a state and returns a vector of resources and a state
# each action requires↲ a cost in resources, and a cost in tick. an agent is frozen during tick cost
# an agent is defined by a memory space that contains both instructions and data. It executes instructions incrementally following a pointer. There may be jump instructions. instructions are sent as a (possibly useless) action to the game, or modify the internal state of the agent.
# if an agent pointer reaches an illegal position, the agent dies

def convert_1d_position_to_2d(
	position,
	column_length
) -> Tuple[int, int]:
	col = position % column_length
	row = position // column_length
	
	return (col, row)

def convert_2d_position_to_1d(
	col_position,
	row_position,
	column_length
) -> int:
	return row_position * column_length + col_position

def cmp_generic_move_to_unsafe_position(
	position,
	column_length,
	offset_col,
	offset_row
) -> int:
	col, row = convert_1d_position_to_2d(position, column_length)

	new_col = col + offset_col
	new_row = row + offset_row

	return  convert_2d_position_to_1d(new_col, new_row, column_length)

def is_valid_1d_position(position, grid_length) -> bool:
	return (0 <= position) and (position < grid_length)


def cmp_generic_move_to_safe_position(
	grid_length,
	position,
	column_length,
	offset_col,
	offset_row
) -> Optional[int]:
	unsafe_position = cmp_generic_move_to_unsafe_position(
		position=position,
		column_length=column_length,
		offset_col=offset_col,
		offset_row=offset_row
	)
	if is_valid_1d_position(unsafe_position, grid_length):
		return unsafe_position
	return None

def cmp_safe_position_on_move_up(agent_pos, grid_length, column_length) -> Optional[int]:
	return cmp_generic_move_to_safe_position(
		grid_length=grid_length,
		position=agent_pos,
		column_length=column_length,
		offset_col=(0),
		offset_row=(-1),
	)

def cmp_safe_position_on_move_down(agent_pos, grid_length, column_length) -> Optional[int]:
	return cmp_generic_move_to_safe_position(
		grid_length=grid_length,
		position=agent_pos,
		column_length=column_length,
		offset_col=(0),
		offset_row=(1),
	)

def cmp_safe_position_on_move_right(agent_pos, grid_length, column_length) -> Optional[int]:
	return cmp_generic_move_to_safe_position(
		grid_length=grid_length,
		position=agent_pos,
		column_length=column_length,
		offset_col=(1),
		offset_row=(0),
	)

def cmp_safe_position_on_move_left(agent_pos, grid_length, column_length) -> Optional[int]:
	return cmp_generic_move_to_safe_position(
		grid_length=grid_length,
		position=agent_pos,
		column_length=column_length,
		offset_col=(-1),
		offset_row=(0),
	)

def snake_iteration(
	actions: List[int],
	state: Dict,
) -> Tuple[List[any], Dict]:
	'''
		For the first version, snakes do not get bigger and do not die if they hit another snake
	'''
	# todo: put ACTION_SET in a nicer place within the module to avoid recreating a dict at each call
	ACTION_SET = dict()
	ACTION_SET[ord('↑')] = cmp_safe_position_on_move_up
	ACTION_SET[ord('→')] = cmp_safe_position_on_move_right
	ACTION_SET[ord('↓')] = cmp_safe_position_on_move_down
	ACTION_SET[ord('←')] = cmp_safe_position_on_move_left

	# destructuration of the state
	agent_positions = state['agent_positions']
	dead_agents = state['dead_agents']
	grid = state['grid']
	grid_column_length = state['grid_column_length']
	grid_row_length = state['grid_row_length']

	# sanity check
	assert len(actions) == len(agent_positions)
	assert len(grid) == (grid_column_length * grid_row_length)


	new_dead_agents = [da for da in dead_agents]
	new_agent_positions = [ap for ap in agent_positions]

	# apply every agent's action if it is still alive
	for agent_id in range(len(agent_positions)):
		if dead_agents[agent_id]:
			continue

		agent_position = agent_positions[agent_id]
		chosen_action = actions[agent_id]

		if chosen_action is None:
			print("chose no action this round")
		else: 
			print(f"chosen action is <{chr(chosen_action)}>")

		if chosen_action not in ACTION_SET:
			continue

		new_position = ACTION_SET[chosen_action](agent_position, len(grid), grid_column_length)
		if new_position is None:
			new_dead_agents[agent_id] = True
			continue
		new_agent_positions[agent_id] = new_position

	# mark agent positions on the grid
	new_grid = [False for _ in grid]
	for agent_id in range(len(agents)):
		agent_position = new_agent_positions[agent_id]
		if not new_dead_agents[agent_id]:
			new_grid[agent_position] = True

	# generate_new_state
	new_state = dict()
	new_state['agent_positions'] = new_agent_positions
	new_state['dead_agents'] = new_dead_agents
	new_state['grid'] = new_grid
	new_state['grid_column_length'] = grid_column_length
	new_state['grid_row_length'] = grid_row_length

	# resources
	new_resources = [None for _ in agent_positions]

	return (new_resources, new_state)


def conditionally_jumps_to_position_if_next_is_0(
	agent_id: int,
	agent: List[int],
	game_state: Dict,
	pointer: int
) -> Optional[Dict[str, int]]:
	'''
		JXP sets pointer to position P if X equals 0, else advances pointer value by 3
		
		on success returns (order, new_agent, new_agent_pointer)
		on failure returns None, meaning that the agent died due to wrongful execution
	'''
	if not ( (pointer + 3) <= len(agent) ):
		return None

	conditional_symbol = agent[pointer + 1] 
	position_symbol = agent[pointer + 2]

	new_pointer = position_symbol if conditional_symbol == 0 else (pointer + 3)

	if not (0 <= new_pointer and new_pointer < len(agent)):
		return None

	output = dict()
	output['order'] = ord('J')
	output['new_agent'] = agent  
	output['new_agent_pointer'] = new_pointer
	return output


def is_neighbor_cell_in_grid(
	grid: List[int],
	grid_column_length: int,
	grid_row_length: int,
	position: int,
	neighbor_symbol: int
) -> bool:
	NEIGHBOR_POSITION_CALCULATORS = dict()
	NEIGHBOR_POSITION_CALCULATORS[ord('↑')] = lambda c, r: (c + 0, r - 1)
	NEIGHBOR_POSITION_CALCULATORS[ord('→')] = lambda c, r: (c + 1, r + 0)
	NEIGHBOR_POSITION_CALCULATORS[ord('↓')] = lambda c, r: (c + 0, r + 1)
	NEIGHBOR_POSITION_CALCULATORS[ord('←')] = lambda c, r: (c - 1, r + 0)
	NEIGHBOR_POSITION_CALCULATORS[ord('↱')] = lambda c, r: (c + 1, r - 1)
	NEIGHBOR_POSITION_CALCULATORS[ord('↲')] = lambda c, r: (c - 1, r + 1)
	NEIGHBOR_POSITION_CALCULATORS[ord('↳')] = lambda c, r: (c + 1, r + 1)
	NEIGHBOR_POSITION_CALCULATORS[ord('↰')] = lambda c, r: (c - 1, r - 1)
	
	col_position, row_position = convert_1d_position_to_2d(position, grid_column_length)
	(neighbor_col_pos, neighbor_row_pos) = NEIGHBOR_POSITION_CALCULATORS[neighbor_symbol](col_position, row_position)
	return ( 
		(0 <= neighbor_col_pos) and (neighbor_col_pos < grid_column_length)
		and
		(0 <= neighbor_row_pos) and (neighbor_row_pos < grid_row_length)
	)


def load_state_at_position(
	agent_id: int,
	agent: List[int],
	game_state: Dict,
	pointer: int
) -> Optional[Dict[str, int]]:
	'''
		LXP writes symbol representing whether position X is valid on game grid to position P of agent memory

		on success returns (order, new_agent, new_agent_pointer)
		on failure returns None, meaning that the agent died due to wrongful execution
	'''

	new_pointer = pointer + 3
	if not (new_pointer < len(agent)):
		return None

	value_symbol = int(
		is_neighbor_cell_in_grid(
			grid=game_state['grid'],
			grid_column_length=game_state['grid_column_length'],
			grid_row_length=game_state['grid_row_length'],
			position = game_state['agent_positions'][agent_id],
			neighbor_symbol = agent[pointer + 1]
		)
	)
	position_symbol = agent[pointer + 2]

	if not (0 <= position_symbol and position_symbol < len(agent)):
		return None

	new_agent = [agent[i] if i != position_symbol else value_symbol for i in range(len(agent))]

	output = dict()
	output['order'] = ord('L')
	output['new_agent'] = new_agent
	output['new_agent_pointer'] = new_pointer
	return output

def submit_instruction(
	agent: List[int],
	pointer: int,
) -> Optional[Dict[str, int]]:
	'''
		on success returns (order, new_agent, new_agent_pointer)
		on failure returns None, meaning that the agent died due to wrongful execution
	'''
	new_pointer = pointer + 1
	if not (new_pointer < len(agent)):
		return None

	instruction_symbol = agent[pointer]

	output = dict()
	output['order'] = instruction_symbol
	output['new_agent'] = agent
	output['new_agent_pointer'] = new_pointer
	return output


def submit_instruction_up(
	agent_id: int,
	agent: List[int],
	game_state: Dict,
	pointer: int
) -> Optional[Dict[str, int]]:
	'''
		↑ advances pointer value by 1 and modifies game state by moving agent up
		
		on success returns (order, new_agent, new_agent_pointer)
		on failure returns None, meaning that the agent died due to wrongful execution
	'''
	return submit_instruction(
		agent=agent,
		pointer=pointer
	)

def submit_instruction_right(
	agent_id: int,
	agent: List[int],
	game_state: Dict,
	pointer: int
) -> Optional[Dict[str, int]]:
	'''
		→ advances pointer value by 1 and modifies game state by moving agent right
		
		on success returns (order, new_agent, new_agent_pointer)
		on failure returns None, meaning that the agent died due to wrongful execution
	'''
	return submit_instruction(
		agent=agent,
		pointer=pointer
	)

def submit_instruction_down(
	agent_id: int,
	agent: List[int],
	game_state: Dict,
	pointer: int
) -> Optional[Dict[str, int]]:
	'''
		↓ advances pointer value by 1 and modifies game state by moving agent down
		
		on success returns (order, new_agent, new_agent_pointer)
		on failure returns None, meaning that the agent died due to wrongful execution
	'''
	return submit_instruction(
		agent=agent,
		pointer=pointer
	)

def submit_instruction_left(
	agent_id: int,
	agent: List[int],
	game_state: Dict,
	pointer: int
) -> Optional[Dict[str, int]]:
	'''
		← advances pointer value by 1 and modifies game state by moving agent left
		
		on success returns (order, new_agent, new_agent_pointer)
		on failure returns None, meaning that the agent died due to wrongful execution
	'''
	return submit_instruction(
		agent=agent,
		pointer=pointer
	)


def iterate(
	# immutable between iterations
	game_iterate,
	instruction_set,
	instruction_costs,

	# mutable between iterations
	agents,
	game_state,
	pointers,
	agents_freeze_values
) -> Dict:
	'''
		For now, resources are ignored
	'''
	actions = [None for _ in agents]
	new_agents = [a for a in agents]
	new_pointers = [p for p in pointers]

	for agent_id in range(len(agents)):
		if game_state['dead_agents'][agent_id]:
			continue

		agents_freeze_values[agent_id] -= 1
		if agents_freeze_values[agent_id] >= 0:
			continue

		current_agent = agents[agent_id]
		current_pointer = pointers[agent_id]
		current_instruction_symbol = current_agent[current_pointer]
		current_instruction_operation = instruction_set[current_instruction_symbol]

		instruction_result = current_instruction_operation(
			agent_id=agent_id,
			agent=current_agent,
			game_state=game_state,
			pointer=current_pointer
		)
		if instruction_result is None:
			game_state['dead_agents'][agent_id] = True
			continue

		actions[agent_id] = instruction_result['order']
		new_agents[agent_id] = instruction_result['new_agent']
		new_pointers[agent_id] = instruction_result['new_agent_pointer']
		agents_freeze_values[agent_id] += instruction_costs[current_instruction_symbol]

	resources, game_state = game_iterate(
		actions=actions,
		state=game_state,
	)

	output = dict()
	output['agents'] = new_agents
	output['game_state'] = game_state
	output['pointers'] = new_pointers
	output['agents_freeze_values'] = agents_freeze_values

	return output

def grid_to_str(grid, grid_column_length):
	out = "[\n\t["
	for i in range(len(grid)):
		out += '🐍' if grid[i] else str(i)
		if i % grid_column_length == (grid_column_length - 1):
			out += "]\n"
			if i != (len(grid) - 1):
				out += "\t["
		else:
			out += '\t'
	out += "]"
	return out


def print_grid(grid, grid_column_length):
	print(grid_to_str(grid, grid_column_length))

def agent_to_str(agent, pointer):
	out = "["
	for i in range(len(agent)):

		out += "\t"
		if pointer == i:
			out += '\033[94m'
		out += str(agent[i])
		if pointer == i:
			out += '\033[0m'
		out += ","

		if i % 10 == 9:
			out +="\n"
	out += "]"
	return out

def print_agent(agent, pointer):
	print(agent_to_str(agent, pointer))

def perform_n_iterations(
	n: int,
	post_iteration_callback: Callable[[Dict], None],

	# immutable between iterations
	game_iterate,
	instruction_set,
	instruction_costs,

	# mutable between iterations
	agents,
	game_state,
	pointers,
	agents_freeze_values
):
	for _ in range(n):
		result = iterate(
			game_iterate=game_iterate,
			instruction_set=instruction_set,
			instruction_costs=instruction_costs,
			agents=agents,
			game_state=game_state,
			pointers=pointers,
			agents_freeze_values=agents_freeze_values,
		)

		post_iteration_callback(result)

		agents = result['agents']
		game_state = result['game_state']
		pointers = result['pointers']
		agents_freeze_values = result['agents_freeze_values']

def debug_post_iteration_callback(result, grid_only=False):
	if not grid_only:
		print("game_state['agent_positions']", result['game_state']['agent_positions'])
		print("game_state['agents']:")
		print_agent(result['agents'][0], result['pointers'][0])
		print("grid:")
	print_grid(result['game_state']['grid'], grid_column_length)


if __name__ == '__main__':
	instruction_set = dict()
	instruction_set[ord('J')] = conditionally_jumps_to_position_if_next_is_0
	instruction_set[ord('L')] = load_state_at_position 
	instruction_set[ord('↑')] = submit_instruction_up
	instruction_set[ord('→')] = submit_instruction_right
	instruction_set[ord('↓')] = submit_instruction_down
	instruction_set[ord('←')] = submit_instruction_left

	instruction_costs = dict()
	instruction_costs[ord('J')] = 10
	instruction_costs[ord('L')] = 3
	instruction_costs[ord('↑')] = 1
	instruction_costs[ord('→')] = 1
	instruction_costs[ord('↓')] = 1
	instruction_costs[ord('←')] = 1


	grid_column_length = 10
	grid_row_length = 10

	n = 100

	game_iterate=snake_iteration
	agents=[
		# [ord('↓') for _ in range(2)] + [ord('←') for _ in range(3)],
		[
			ord('L'), ord('↑'),  4, ord('J'), ord('-'), 10, ord('↑'), ord('J'), 0,  0,
			ord('L'), ord('→'), 14, ord('J'), ord('-'), 20, ord('→'), ord('J'), 0, 10,
			ord('L'), ord('↓'), 24, ord('J'), ord('-'), 30, ord('↓'), ord('J'), 0, 20,
			ord('L'), ord('←'), 34, ord('J'), ord('-'), 00, ord('←'), ord('J'), 0, 30
		]
	]
	for agent in agents:
		for symbol in agent:
			print(f"`{chr(symbol)}", end="`,\t")
	print("")
	pointers = [0 for _ in agents]
	agents_freeze_values = [0 for _ in agents]

	game_state = dict()
	game_state['dead_agents'] = [False for _ in agents]
	game_state['grid'] = [0 for _ in range(grid_column_length * grid_row_length)]
	game_state['grid_column_length'] = grid_column_length
	game_state['grid_row_length'] = grid_row_length
	game_state['agent_positions'] = [
		# convert_2d_position_to_1d(5, 5, grid_column_length),
		convert_2d_position_to_1d(0, 0, grid_column_length)
	]

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

# # if going up and if obstructed up and right, turn left
# # if going up and if obstructed up and left, turn right
# 012
# LU4
# 345
# J-P
# 6
# U
# 789
# J00
# # apply same principle
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

# if going right and if obstructed right and up, turn down
# if going right and if obstructed right and down, turn up

# if going down and if obstructed down and right, turn left
# if going down and if obstructed down and left, turn right

# if going left and if obstructed left and up, turn down
# if going left and if obstructed left and down, turn up
