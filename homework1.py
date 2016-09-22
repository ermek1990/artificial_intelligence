from collections import OrderedDict

import heapq

# Took this import code from www.bogotobogo.com
try:
    from Queue import PriorityQueue
except ImportError:
    from queue import PriorityQueue


# Used this class from stackoverflow to create custom OrderedDict with behavior of defaultdict
class CustomDict(OrderedDict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


class NodeQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node):
        self.nodes.insert(0, node)

    def get(self):
        return self.nodes.pop()

    def empty(self):
        return not self.nodes

    def ext(self, node):
        self.nodes.append(node)

    def is_exist(self, node):
        return node in self.nodes

    def next_node(self):
        return self.nodes[len(self.nodes) - 1]


def func_is_empty_file():
    try:
        file_obj = open(file_name)
        input_d = ''
        try:
            input_d = file_obj.read()
        finally:
            file_obj.close()
            return input_d == ''
    except IOError:
        print('The file does not exist.')


def func_write_file(output_data):
    try:
        file_obj = open('output.txt', 'w')
        try:
            file_obj.write(output_data)
        finally:
            file_obj.close()
    except IOError:
        print('Cannot write the output data into file.')


def func_print_file_content(file_name):
    try:
        file_obj = open(file_name)
        try:
            print(file_obj.read())
        finally:
            file_obj.close()
    except IOError:
        print('The file does not exist.')


def func_get_line_from_file(file_obj, desired_line):
    if desired_line < 1:
        return ''
    for curr_line, line in enumerate(file_obj):
        if curr_line == desired_line - 1:
            return line
    return ''


def func_create_lines_list(file_obj, line_count):
    traffic_list = list([])
    for lineNum in range(0, line_count):
        traffic_list.append(str.split(func_get_line_from_file(file_obj, 1)))
    return traffic_list


def func_create_node_dict(line_list):
    nodes = CustomDict()
    for i, node in enumerate(line_list):
        nodes[node[0]].append(node[1])
    return nodes


def func_create_node_dict_astar(line_list):
    nodes = CustomDict()
    for i, node in enumerate(line_list):
        nodes[node[0]].append(node[1])
    return nodes


def func_bfs(nodes, start_node, goal_node):
    output = ''
    path_memo, nodes_visited, node_q = [], [start_node], NodeQueue()
    node_q.put(nodes_visited)
    while not node_q.empty():
        nodes_visited = node_q.get()
        prev_node = nodes_visited[len(nodes_visited) - 1]
        if prev_node == goal_node:
            path_memo.append(nodes_visited)
        for node in nodes[prev_node]:
            if node not in nodes_visited:
                path = nodes_visited + [node]
                node_q.put(path)
    for i in range(0, len(path_memo)):
        if len(path_memo[i]) == min(map(len, path_memo)):
            for j in range(0, len(path_memo[i])):
                output += path_memo[i][j] + ' ' + str(j) + '\n'
            break
    return output


def func_print_dfs(parents_set, start_node, goal_node):
    total_path = [goal_node]
    node = goal_node
    while node != start_node:
        total_path.append(parents_set[node])
        node = parents_set[node]
    total_path.reverse()
    output = ''
    for i in range(0, len(total_path)):
        output += total_path[i] + ' ' + str(i) + '\n'
    return output


def func_dfs(nodes, start_node, goal_node):
    for node_key in nodes.keys():
        nodes[node_key].reverse()
    nodes_visited = []
    nodes_stack = NodeQueue()
    nodes_stack.ext(start_node)
    parents = {start_node: ''}
    while not nodes_stack.empty():
        node = nodes_stack.get()
        if not nodes_stack.is_exist(node):
            if node not in nodes_visited:
                nodes_visited = nodes_visited + [node]
                temp = [n for n in nodes[node] if n not in nodes_visited]
                for i in range(0, len(temp)):
                    if not nodes_stack.is_exist(temp[i]):
                        parents[temp[i]] = node
                        if temp[i] == goal_node:
                            return func_print_dfs(parents, start_node, goal_node)
                        nodes_stack.ext(temp[i])


def func_get_edge_cost(e_1, e_2, edge_set):
    cost = 0
    for edge in edge_set:
        if edge[0] == e_1 and edge[1] == e_2:
            cost = edge[2]
            break
    return cost


def func_construct_path_astar(path, node, final_len):
    total_path = [[node, final_len]]
    while node in path.keys():
        instance = path[node]
        node = instance[0]
        distance = instance[1]
        total_path.append([node, distance])
    total_path.reverse()
    output = ''
    for i in range(0, len(total_path)):
        output += total_path[i][0] + ' ' + str(total_path[i][1]) + '\n'
    return output


def func_construct_path_ucs(path, start_node, goal_node):
    total_path = []
    node = goal_node
    while node in path.keys():
        instance = path[node]
        total_path.append([node, instance[1]])
        node = instance[0]
    total_path.append([start_node, 0])
    total_path.reverse()
    output = ''
    for i in range(0, len(total_path)):
        output += total_path[i][0] + ' ' + str(total_path[i][1]) + '\n'
    return output


def func_astar(nodes, edge_costs, h_values, start_node, goal_node):
    output = ''
    open_heap, open_set, evaluated_nodes, g_score, f_score, path_memo = [], set(), set(), {}, {}, {}
    node_d = {0: start_node}
    n_counter = 1
    heapq.heappush(open_heap, (0, 0))
    open_set.add(start_node)
    f_score[start_node] = h_values[start_node]
    g_score[start_node] = 0
    while open_set:
        current_value, current_node_d = heapq.heappop(open_heap)
        current_node = node_d[current_node_d]
        if current_node == goal_node:
            output = func_construct_path_astar(path_memo, current_node, current_value)
            break
        open_set.discard(current_node)
        evaluated_nodes.add(current_node)
        for neighbor_node in nodes[current_node]:
            if neighbor_node not in evaluated_nodes:
                tentative_gscore = current_value + int(func_get_edge_cost(current_node, neighbor_node, edge_costs))
                if neighbor_node not in open_set:
                    open_set.add(neighbor_node)
                elif tentative_gscore >= g_score[neighbor_node]:
                    continue
                heapq.heappush(open_heap, (tentative_gscore, n_counter))
                node_d[n_counter] = neighbor_node
                n_counter += 1
                g_score[neighbor_node] = tentative_gscore
                f_score[neighbor_node] = tentative_gscore + h_values[neighbor_node]
                path_memo[neighbor_node] = [current_node, g_score[current_node]]
    return output


def func_ucs(nodes, edge_costs, start_node, goal_node):
    output, nodes_visited, node_q, path_memo = '', [], PriorityQueue(), {}
    node_q.put((0, 0))
    node_d = {0: start_node}
    n_counter = 1
    while not node_q.empty():
        edge_cost, current_node_d = node_q.get()
        current_node = node_d[current_node_d]
        if current_node == goal_node:
            output = func_construct_path_ucs(path_memo, start_node, current_node)
            break
        for neighbor_node in nodes[current_node]:
            if neighbor_node not in nodes_visited:
                nodes_visited.append(neighbor_node)
                total_node_cost = int(func_get_edge_cost(current_node, neighbor_node, edge_costs)) + edge_cost
                node_q.put((total_node_cost, n_counter))
                node_d[n_counter] = neighbor_node
                n_counter += 1
                path_memo[neighbor_node] = [current_node, total_node_cost]
    return output


file_name = 'input.txt'
if not func_is_empty_file():
    # func_print_file_content(file_name)
    file_inst = open(file_name, 'rU')
    algo = func_get_line_from_file(file_inst, 1).rstrip()
    start_state = func_get_line_from_file(file_inst, 1).rstrip()
    goal_state = func_get_line_from_file(file_inst, 1).rstrip()
    output_data = ''
    if start_state == goal_state:
        output_data = start_state + ' 0'
    else:
        line_list = func_create_lines_list(file_inst, int(func_get_line_from_file(file_inst, 1).rstrip()))
        if algo == 'BFS':
            node_dict = func_create_node_dict(line_list)
            output_data = func_bfs(node_dict, start_state, goal_state)
        elif algo == 'DFS':
            node_dict = func_create_node_dict(line_list)
            output_data = func_dfs(node_dict, start_state, goal_state)
        elif algo == 'A*':
            node_dict = func_create_node_dict(line_list)
            heuristic_list = func_create_lines_list(file_inst, int(func_get_line_from_file(file_inst, 1).rstrip()))
            heuristic_values = dict((x[0], (int(x[1]))) for x in heuristic_list[0:])
            output_data = func_astar(node_dict, line_list, heuristic_values, start_state, goal_state)
        elif algo == 'UCS':
            node_dict = func_create_node_dict(line_list)
            output_data = func_ucs(node_dict, line_list, start_state, goal_state)
        else:
            print('The algorithm in the input file is incorrect.')
    if output_data != '':
        func_write_file(output_data)
        func_print_file_content('output.txt')
else:
    print('Something went wrong. Either the file is empty or corrupted.')
