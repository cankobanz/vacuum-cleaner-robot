import sys
search_type = sys.argv[1]
initial_state_path = sys.argv[2]
file = open(initial_state_path)


grid_world_raw = file.readlines()

start_r = None
start_c = None

N = 0  # Number of dirts in the grid world.

dirt_locations = []
grid_world = []
for r in range(len(grid_world_raw)):
    line = []
    if grid_world_raw[r][-1] == '\n':
        grid_world_raw[r] = grid_world_raw[r][:-1]
    grid_world.append(line)
    for c in range(len(grid_world_raw[r])):
        line.append(grid_world_raw[r][c])
        if grid_world_raw[r][c] == 'c':
            grid_world[r][c] = ' '
            start_r = r
            start_c = c
        if grid_world_raw[r][c].isdigit():
            dirt_locations.append((r, c))
            N += int(grid_world_raw[r][c])


def create_goal_state(data):
    copy_map = []
    for r in range(0, len(data)):
        line = []
        copy_map.append(line)
        for c in range(0, len(data[r])):
            if data[r][c].isdigit():
                line.append(' ')
            else:
                line.append(data[r][c])
    return copy_map


goal_state = create_goal_state(grid_world)

R = len(grid_world)
C = len(grid_world[0])


class Node:
    def __init__(self, row, column, data):
        self.data = self.create_copy_map(data)
        self.location = (row, column)

        self.state = (self.location, self.data)

        self.dirt_locations = self.find_dirt_locations()

        self.cost = 0
        self.heuristic = self.calculate_manhattan()
        self.combined_heuristic = self.cost + self.heuristic
        self.my_heuristic = self.cost + self.my_calculate_manhattan()
        self.action = None
        self.parent = None

    def isDirt(self):
        if self.data[self.location[0]][self.location[1]].isdigit():
            return True
        else:
            return False

    def remove_dirt(self):
        nDirts = int(self.data[self.location[0]][self.location[1]])
        nDirts -= 1
        self.data[self.location[0]][self.location[1]] = str(nDirts)
        if nDirts == 0:
            self.data[self.location[0]][self.location[1]] = ' '

    def find_path(self):
        def reverse_list(got_list):
            temp = []
            while got_list:
                temp.append(got_list.pop())
            return temp

        path = [self.action]
        current_node = self.parent
        while current_node.parent is not None:
            path.append(current_node.action)
            current_node = current_node.parent
        return reverse_list(path)

    def find_dirt_locations(self):
        temp_dirt_locations = []
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                if self.data[r][c].isdigit():
                    temp_dirt_locations.append((r, c))
        return temp_dirt_locations

    def calculate_manhattan(self):
        manhattan = float('inf')
        for dirt_loc in self.dirt_locations:
            dirt_r = dirt_loc[0]
            dirt_c = dirt_loc[1]
            temp_manhattan = abs(dirt_r - self.location[0]) + abs(dirt_c - self.location[1])
            if temp_manhattan < manhattan:
                manhattan = temp_manhattan
        return manhattan

    def my_calculate_manhattan(self):
        manhattan = float('inf')
        for dirt_loc in self.dirt_locations:
            dirt_r = dirt_loc[0]
            dirt_c = dirt_loc[1]
            temp_manhattan =  2 * abs(dirt_r - self.location[0]) + abs(dirt_c - self.location[1])
            if temp_manhattan < manhattan:
                manhattan = temp_manhattan
        return manhattan

    @staticmethod
    def create_copy_map(data):
        copy_map = []
        for r in range(0, len(data)):
            line = []
            copy_map.append(line)
            for c in range(0, len(data[r])):
                line.append(data[r][c])
        return copy_map


def check_exist_in_frontier(node, queue):
    for element in queue:
        if element.state == node.state:
            return queue.index(element)


def actions(current_node):
    current_r, current_c = current_node.location

    children = []

    dr = [0, 0, 0, 1, -1]
    dc = [0, -1, +1, 0, 0]

    for i in range(0, 5):

        possible_r = current_r + dr[i]
        possible_c = current_c + dc[i]

        if grid_world[possible_r][possible_c] == 'j':
            possible_r = possible_r + dr[i]
            possible_c = possible_c + dc[i]

        # Check it is not out of bounds.
        if possible_r < 0 or possible_c < 0:
            continue
        if possible_r >= R or possible_c >= C:
            continue
        if grid_world[possible_r][possible_c] == 'x':
            continue

        child = Node(possible_r, possible_c, current_node.data)
        child.parent = current_node
        if i == 0 and child.isDirt():
            child.action = "suck"
            child.remove_dirt()
            child.cost = child.parent.cost + 5
            children.append(child)
        elif i == 1:
            child.action = "left"
            child.cost = child.parent.cost + 1
            children.append(child)
        elif i == 2:
            child.action = "right"
            child.cost = child.parent.cost + 1
            children.append(child)
        elif i == 3:
            child.action = "down"
            child.cost = child.parent.cost + 2
            children.append(child)
        elif i == 4:
            child.action = "up"
            child.cost = child.parent.cost + 2
            children.append(child)

    return children


def bfs():
    start_node = Node(start_r, start_c, grid_world)

    visited = []
    queue = [start_node]
    while queue:
        current_node = queue.pop(0)

        if current_node.state[1] == goal_state:
            return len(visited), current_node.find_path(), current_node.cost

        if current_node.state not in visited:
            visited.append(current_node.state)

        children = actions(current_node)

        for child in children:
            if child.state not in visited:
                queue.append(child)


def dfs():
    start_node = Node(start_r, start_c, grid_world)

    visited = []
    stack = [start_node]
    while stack:
        current_node = stack.pop()

        if current_node.state[1] == goal_state:
            return len(visited), current_node.find_path(), current_node.cost

        if current_node.state not in visited:
            visited.append(current_node.state)

        children = actions(current_node)

        for child in children:
            if child.state not in visited:
                stack.append(child)


def ucs():
    start_node = Node(start_r, start_c, grid_world)

    visited = []
    p_queue = [start_node]
    while p_queue:
        p_queue = sorted(p_queue, key=lambda x: x.cost)
        current_node = p_queue.pop(0)

        if current_node.state[1] == goal_state:
            return len(visited), current_node.find_path(), current_node.cost

        if current_node.state not in visited:
            visited.append(current_node.state)

        children = actions(current_node)

        for child in children:
            if child.state not in visited:
                p_queue.append(child)


def gs():
    start_node = Node(start_r, start_c, grid_world)

    visited = []
    p_queue = [start_node]
    while p_queue:
        p_queue = sorted(p_queue, key=lambda x: x.heuristic)
        current_node = p_queue.pop(0)

        if current_node.state[1] == goal_state:
            return len(visited), current_node.find_path(), current_node.cost

        if current_node.state not in visited:
            visited.append(current_node.state)

        children = actions(current_node)

        for child in children:
            if child.state not in visited:
                p_queue.append(child)


def a_star():
    start_node = Node(start_r, start_c, grid_world)

    visited = []
    p_queue = [start_node]
    while p_queue:
        p_queue = sorted(p_queue, key=lambda x: x.combined_heuristic)
        current_node = p_queue.pop(0)

        if current_node.state[1] == goal_state:
            return len(visited), current_node.find_path(), current_node.cost

        if current_node.state not in visited:
            visited.append(current_node.state)

        children = actions(current_node)

        for child in children:
            if child.state not in visited:
                p_queue.append(child)


def a_star_my():
    start_node = Node(start_r, start_c, grid_world)

    visited = []
    p_queue = [start_node]
    initial_heuristic = start_node.my_heuristic
    while p_queue:
        p_queue = sorted(p_queue, key=lambda x: x.my_heuristic)
        current_node = p_queue.pop(0)

        if current_node.state[1] == goal_state:
            return len(visited), current_node.find_path(), current_node.cost, initial_heuristic

        if current_node.state not in visited:
            visited.append(current_node.state)

        children = actions(current_node)

        for child in children:
            if child.state not in visited:
                p_queue.append(child)

expanded_nodes = None
path = None
cost = None
initial_heuristic=None
if(search_type == "BFS"):
    expanded_nodes, path, cost = bfs()
elif(search_type == "DFS"):
    expanded_nodes, path, cost = dfs()
elif(search_type == "UCS"):
    expanded_nodes, path, cost = ucs()
elif(search_type == "GS"):
    expanded_nodes, path, cost = gs()
elif(search_type == "A*1"):
    expanded_nodes, path, cost = a_star()
elif(search_type == "A*2"):
    expanded_nodes, path, cost, initial_heuristic = a_star_my()


print(f"number of expanded nodes: {expanded_nodes}")
print("path:", end=' ')
print(*path, sep=' ')
print(f"cost of the solution: {cost}")
if(search_type == "A*2"):
    print(f"heuristic of initial state: {initial_heuristic}")