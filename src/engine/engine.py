# each tick, game takes vector of actions and a state and returns a vector of resources and a state
# each action requires↲ a cost in resources, and a cost in tick. an agent is frozen during tick cost
# an agent is defined by a memory space that contains both instructions and data. It executes instructions incrementally following a pointer. There may be jump instructions. instructions are sent as a (possibly useless) action to the game, or modify the internal state of the agent.
# if an agent pointer reaches an illegal position, the agent dies

from typing import Callable, Dict

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
