from typing import Dict, Optional, List

from utils.grid_utils import convert_1d_position_to_2d

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
	output['order'] = None
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
	output['order'] = None
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
