#!usr/bin/env python
####################################
# Sailesh Dhungana (Week 2 Project)#
####################################

import sys
import resource
from collections import deque

class PriorityQueue:

	def __init__(self):
		self.array = [None]
		self.position_map = {}
		self.size = 0

	def is_empty(self):
		return self.size == 0

	def exchange(self, position_a, position_b):
		a = self.array[position_a]
		b = self.array[position_b]
		dummy = a		
		self.array[position_a] = b
		self.array[position_b] = dummy
		self.position_map[a[1].board_values] = position_b
		self.position_map[b[1].board_values] = position_a

	def UDLR(self, position_a, position_b):
		state_a = self.array[position_a][1]
		state_b = self.array[position_b][1]
		UDLR_dict = {"'Up'": 4, "'Down'": 3, "'Left'": 2, "'Right'": 1, None: 0}
		udlr = UDLR_dict[Board.get_action_from_parent(state_a)] - \
			UDLR_dict[Board.get_action_from_parent(state_b)]
		if udlr > 0:
			return True
		else:
			return False

	def swim(self, position, key, state):
		if position == 1:
			self.position_map[state.board_values] = position
		while position > 1:
			key_difference = self.array[position][0] - self.array[position/2][0]
			if key_difference < 0 or (key_difference == 0 and self.UDLR(position, position/2)):
					self.exchange(position, position/2)
					position = position/2
			else:
				self.position_map[state.board_values] = position
				break

	def sink(self, position):
		current_key = self.array[position][0]
		swap_position = 2 * position
		while swap_position <= self.size:
			swap_key, swap_child = self.array[swap_position]
			if swap_position + 1 <= self.size:
				swap_key_2, swap_child_2 = self.array[swap_position + 1]
				if swap_key_2 < swap_key or (swap_key == swap_key_2 and self.UDLR(swap_position + 1, swap_position)):
					swap_key = swap_key_2
					swap_position = swap_position + 1
			if current_key > swap_key or (current_key == swap_key and self.UDLR(swap_position, position)):
				self.exchange(position, swap_position)
				position = swap_position
				swap_position *= 2 
			else:
				break



	def put(self, key, state):
		self.array.append((key, state))
		self.size += 1
		self.swim(self.size, key, state)

	def get(self):
		if self.size > 1:
			self.exchange(1, self.size)
			minimum = self.array.pop()
			self.size -= 1
			self.sink(1)
		else:
			self.size -= 1
			minimum = self.array.pop()

		del self.position_map[minimum[1].board_values]
		return minimum[1]
		
	def update(self, new_key, state):
		position = self.position_map[state.board_values]
		self.array[position] = (new_key, state)

		old_minimum = self.array[1]
		self.exchange(position, 1)
		self.swim(position, old_minimum[0], old_minimum[1])
		#new key brought down to 1 or 2 or 3
		if self.array[1][1].board_values == state.board_values:
			self.sink(1)
		elif self.array[2][1].board_values == state.board_values:
			self.sink(2)
		else:
			self.sink(3)

class Solver:

	def __init__(self, initial_state, search_method):
		self.initial_state = initial_state
		self.search_method = search_method
		self.nodes_expanded = 0
		self.max_search_depth = 0


	def solve(self):
		if self.search_method == "bfs":
			self.bfs_solve()
		if self.search_method == "dfs":
			self.dfs_solve()
		if self.search_method == "ast":
			self.ast_solve()

	def bfs_solve(self):
		frontier = deque()
		frontier.append(self.initial_state)
		frontier_dict = {self.initial_state.board_values:0}
		explored_dict = {}

		while frontier:
			current_state = frontier.popleft()
			explored_dict[current_state.board_values] = 0
			del frontier_dict[current_state.board_values]

			if Board.is_goal_state(current_state):
				self.goal_state = current_state
				return

			self.nodes_expanded += 1
			for child in Board.get_children_UDLR(current_state):
				if self.max_search_depth < child.depth:
					self.max_search_depth = child.depth
				if child.board_values not in explored_dict and\
					child.board_values not in frontier_dict:
						frontier.append(child)
						frontier_dict[child.board_values] = 0

	def dfs_solve(self):
		frontier = []
		frontier.append(self.initial_state)
		frontier_dict = {self.initial_state.board_values:0}
		explored_dict = {}

		while frontier:
			current_state = frontier.pop()
			explored_dict[current_state.board_values] = 0
			del frontier_dict[current_state.board_values]

			if self.max_search_depth < current_state.depth:
				self.max_search_depth = current_state.depth

			if Board.is_goal_state(current_state):
				self.goal_state = current_state
				return

			self.nodes_expanded += 1
			for child in Board.get_children_RLDU(current_state):
				if child.board_values not in explored_dict and\
					child.board_values not in frontier_dict:
						frontier.append(child)
						frontier_dict[child.board_values] = 0

	def ast_solve(self):
		frontier = PriorityQueue()
		current = self.initial_state
		cost = current.depth + Board.get_manhattan_distance(current)
		frontier.put(cost, current)
		explored_dict = {}
		frontier_dict = {current.board_values : 0}

		while not frontier.is_empty():
			current = frontier.get()
			explored_dict[current.board_values] = 0
			del frontier_dict[current.board_values]
			if Board.is_goal_state(current):
				self.goal_state = current
				return

			self.nodes_expanded += 1
			for child in Board.get_children_UDLR(current):
				if self.max_search_depth < child.depth:
					self.max_search_depth = child.depth
				if child.board_values not in explored_dict and\
					child.board_values not in frontier_dict:
						cost = child.depth + Board.get_manhattan_distance(child)
						frontier.put(cost, child)
						frontier_dict[child.board_values] = 0
				elif child.board_values in frontier_dict:
					cost = child.depth + Board.get_manhattan_distance(child)
					current_cost = frontier.array[frontier.position_map[child.board_values]][0]
					if cost < current_cost:
						frontier.update(cost, child)


	def print_result(self):
		path = []
		current = self.goal_state
		while current.parent != None:
			path.append(Board.get_action_from_parent(current))
			current = current.parent
		path = path[::-1]
		string_to_write = 'path_to_goal: [' + ', '.join(path) + ']\n'
		string_to_write += 'cost_of_path: ' + str(len(path)) + '\n'
		string_to_write += 'nodes_expanded: ' + str(self.nodes_expanded) + '\n'
		string_to_write += 'search_depth: ' + str(len(path)) + '\n'
		string_to_write += 'max_search_depth: ' + str(self.max_search_depth) + '\n'
		usage_details = resource.getrusage(resource.RUSAGE_SELF)
		string_to_write += 'running_time: %.8f\n' % (usage_details.ru_utime + usage_details.ru_stime)
		string_to_write += 'max_ram_usage: %.8f\n' % (usage_details.ru_maxrss/1024.0**2)
		
		file = open('output.txt', 'w')
		file.write(string_to_write)
		file.close()

class State:

	def __init__(self, board_values, parent=None):
		self.board_values = board_values
		self.board = map(lambda x: int(x), board_values.split(','))
		self.parent = parent
		if parent == None:
			self.depth = 0
		else:
			self.depth = parent.depth + 1

class Board:

	@classmethod
	def is_goal_state(self, state):
		goal_state = [0,1,2,3,4,5,6,7,8]
		for i in range(9):
			if state.board[i] != goal_state[i]:
				return False
		return True

	@classmethod
	def get_zero_position(self, state):
		# Find position of 0
		for i in range(9):
			if state.board[i] == 0:
				return i

	@classmethod
	def get_swap_positions_UDLR(self, state):
		zero_position = Board.get_zero_position(state)

		# Find surrounding postions that can be swapped with 0
		swaps_lookup_UDLR = {	0:[3,1],
									 	1:[4,0,2],
									 	2:[5,1],
									 	3:[0,6,4],
									 	4:[1,7,3,5],
									 	5:[2,8,4],
									 	6:[3,7],
									 	7:[4,6,8],
									 	8:[5,7]
								 	  }

		return swaps_lookup_UDLR[zero_position]

	@classmethod
	def get_children_UDLR(self, state):
		zero_position = Board.get_zero_position(state)
		swap_positions_UDLR = Board.get_swap_positions_UDLR(state)

		children = []
		for swap_position in swap_positions_UDLR:
			new_board = state.board[:]
			new_board[zero_position] = state.board[swap_position]
			new_board[swap_position] = 0
			new_board = map(lambda x: str(x), new_board)
			new_board = ",".join(new_board)
			children.append(State(new_board, state))

		return children

	@classmethod
	def get_children_RLDU(self, state):
		return Board.get_children_UDLR(state)[::-1]

	@classmethod
	def equals(self, state, another_state):
		if another_state == None:
			return False
		if state.board_values.hash == another_state.board_values.hash:
			if state.board_values == another_state.board_values:
				return True
		else:
			return False

	@classmethod
	def get_action_from_parent(self, state):
		z_state = Board.get_zero_position(state)
		if state.parent == None:
			return None
		else:
			z_parent = Board.get_zero_position(state.parent)
			if z_state == z_parent - 3:
				return "'Up'"
			if z_state == z_parent + 3:
				return "'Down'"
			if z_state == z_parent - 1:
				return "'Left'"
			if z_state == z_parent + 1:
				return "'Right'"

	@classmethod
	def get_manhattan_distance(self, state):
		distance = 0
		for position, tile in enumerate(state.board):
			vertical = position / 3 - tile / 3
			vertical = (-1) * vertical if vertical < 0 else vertical
			horizontal = (position % 3) - (tile % 3)
			horizontal = (-1) * horizontal if horizontal < 0 else horizontal
			distance += vertical + horizontal
		return distance

if __name__ == "__main__":
	search_method = sys.argv[1]
	board_values = sys.argv[2]
	initial_state = State(board_values)
	solver = Solver(initial_state, search_method)
	solver.solve()
	solver.print_result()


