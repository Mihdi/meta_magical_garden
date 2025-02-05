def grid_to_str(grid, grid_column_length):
	out = "[\n\t["
	for i in range(len(grid)):
		if grid[i] == 0:
			out += str(i)
		if grid[i] == 1:
			out += '🐍'
		if grid[i] == 2:
			out += '🍎'
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


def debug_post_iteration_callback(result, grid_only=False):
	if not grid_only:
		print("game_state['agent_positions']", result['game_state']['agent_positions'])
		print("game_state['agents']:")
		print_agent(result['agents'][0], result['pointers'][0])
		print("grid:")
	grid_column_length = result['game_state']['grid_column_length']
	print_grid(result['game_state']['grid'], grid_column_length)
