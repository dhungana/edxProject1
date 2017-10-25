# edxProject1
Week 2 Project of edX (Columbia) Artificial Intelligence Course that got 100%. Implemented BFS, DFS, A* searches (as well as Priority Queue) to solve 8 board puzzle. http://mypuzzle.org/sliding has an example of that game.

# Instruction
Your job in this assignment is to write driver.py, which solves any 8-puzzle board when given an arbitrary starting configuration. The program will be executed as follows:


```$ python driver.py <method> <board>```

The method argument will be one of the following. You need to implement all three of them:

	1. bfs (Breadth-First Search)
	
	2. dfs (Depth-First Search)
	
	3. ast (A-Star Search)
	

The board argument will be a comma-separated list of integers containing no spaces. For example, to use the bread-first search strategy to solve the input board given by the starting configuration {0,8,7,6,5,4,3,2,1}, the program will be executed like so (with no spaces between commas):

```$ python driver.py bfs 0,8,7,6,5,4,3,2,1```

# Output
When executed, your program will create / write to a file called output.txt, containing the following statistics:

	1. path_to_goal: the sequence of moves taken to reach the goal
	
	2. cost_of_path: the number of moves taken to reach the goal
	
	3. nodes_expanded: the number of nodes that have been expanded
	
	4. search_depth: the depth within the search tree when the goal node is found
	
	5. max_search_depth:  the maximum depth of the search tree in the lifetime of the algorithm
	
	6. running_time: the total running time of the search instance, reported in seconds
	
	7. max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes
	
