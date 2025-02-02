from typing import Dict, Optional, List, Tuple
from utils.grid_utils import convert_1d_position_to_2d, convert_2d_position_to_1d

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
	for agent_id in range(len(actions)):
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
