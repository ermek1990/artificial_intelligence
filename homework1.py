from collections import OrderedDict


def func_is_empty_file():
    try:
        file_obj = open('input3.txt')
        try:
            input_data = file_obj.read()
        finally:
            file_obj.close()
            return input_data == ''
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


def func_create_traffic_line_list(file_obj, line_count):
    traffic_list = list([])
    for lineNum in range(0, line_count):
        traffic_list.append(str.split(func_get_line_from_file(file_obj, 1)))
    return traffic_list


# Used this class from stackoverflow to create custom ordered dictionary with behavior of default dictionary
class CustomDict(OrderedDict):
    def __missing__(self, i):
        self[i] = []
        return self[i]


def func_create_node_dict(line_list):
    nodes = CustomDict()
    for i, node in enumerate(line_list):
        nodes[node[0]].append(node[1])
    return nodes


# That's what I've used before
# def func_create_node_dict(line_list):
#     from collections import defaultdict
#     nodes = defaultdict()
#     for i, node in enumerate(line_list):
#         nodes[node[0]].append(node[1])
#     return nodes


class NodeQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node):
        self.nodes.insert(0, node)

    def get(self):
        return self.nodes.pop()

    def empty(self):
        return not self.nodes


class NodeStack:
    def __init__(self):
        self.nodes = []

    def put(self, node):
        self.nodes.extend(node)

    def get(self):
        return self.nodes.pop()

    def empty(self):
        return not self.nodes


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


def func_dfs(nodes, start_node, goal_node):
    # Reversing the order of lists in dictionary
    for node_keys in nodes.keys():
        nodes[node_keys].reverse()
    nodes_visited = []
    nodes_stack = NodeStack()
    nodes_stack.put(start_node)
    while not nodes_stack == []:
        node = nodes_stack.get()
        if node == goal_node:
            nodes_visited.append(node)
            break
        if node not in nodes_visited:
            nodes_visited = nodes_visited + [node]
            # nodes[node].reverse()
            nodes_stack.put(n for n in nodes[node] if n not in nodes_visited)
    output = ''
    for i in range(0, len(nodes_visited)):
        output += nodes_visited[i] + ' ' + str(i) + '\n'
    return output


def func_astar(nodes, start_node, goal_node):
    return ''


def func_ucs(nodes, start_node, goal_node):
    return ''


if not func_is_empty_file():
    func_print_file_content('input3.txt')
    file_inst = open('input3.txt', 'rU')
    algo = func_get_line_from_file(file_inst, 1).rstrip()
    start_state = func_get_line_from_file(file_inst, 1).rstrip()
    goal_state = func_get_line_from_file(file_inst, 1).rstrip()
    output_data = ''
    if start_state == goal_state:
        output_data = start_state + ' 0'
    line_count = func_get_line_from_file(file_inst, 1).rstrip()
    line_list = func_create_traffic_line_list(file_inst, int(line_count))
    print(line_list)
    node_dict = func_create_node_dict(line_list)
    print(node_dict)
    if algo == 'BFS':
        output_data = func_bfs(node_dict, start_state, goal_state)
    elif algo == 'DFS':
        output_data = func_dfs(node_dict, start_state, goal_state)
    elif algo == 'A*':
        func_astar(node_dict, start_state, goal_state)
    elif algo == 'UCS':
        func_ucs(node_dict, start_state, goal_state)
    else:
        print('The algorithm in the input file is incorrect.')
    if output_data != '':
        func_write_file(output_data)
        func_print_file_content('output.txt')
else:
    print('Something went wrong. Either the file is empty or corrupted.')
