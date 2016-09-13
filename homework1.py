from collections import OrderedDict


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
        self.nodes.extend(node)


def func_is_empty_file():
    try:
        file_obj = open(file_name)
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


def func_dfs(nodes, start_node, goal_node):
    # Reversing the order of lists in dictionary
    for node_keys in nodes.keys():
        nodes[node_keys].reverse()
    nodes_visited = []
    nodes_stack = NodeQueue()
    nodes_stack.ext(start_node)
    while not nodes_stack == []:
        node = nodes_stack.get()
        if node == goal_node:
            nodes_visited.append(node)
            break
        if node not in nodes_visited:
            nodes_visited = nodes_visited + [node]
            nodes_stack.ext(n for n in nodes[node] if n not in nodes_visited)
    output = ''
    for i in range(0, len(nodes_visited)):
        output += nodes_visited[i] + ' ' + str(i) + '\n'
    return output


def func_astar(nodes, start_node, goal_node):
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


def func_ucs(nodes, start_node, goal_node):
    return ''

file_name = 'input.txt'
if not func_is_empty_file():
    func_print_file_content(file_name)
    file_inst = open(file_name, 'rU')
    algo = func_get_line_from_file(file_inst, 1).rstrip()
    start_state = func_get_line_from_file(file_inst, 1).rstrip()
    goal_state = func_get_line_from_file(file_inst, 1).rstrip()
    output_data = ''
    if start_state == goal_state:
        output_data = start_state + ' 0'
    else:
        line_list = func_create_traffic_line_list(file_inst, int(func_get_line_from_file(file_inst, 1).rstrip()))
        print(line_list)
        if algo == 'BFS':
            node_dict = func_create_node_dict(line_list)
            print(node_dict)
            output_data = func_bfs(node_dict, start_state, goal_state)
        elif algo == 'DFS':
            node_dict = func_create_node_dict(line_list)
            print(node_dict)
            output_data = func_dfs(node_dict, start_state, goal_state)
        elif algo == 'A*':
            node_dict = func_create_node_dict(line_list)
            print(node_dict)
            sun_line_list = func_create_traffic_line_list(file_inst, int(func_get_line_from_file(file_inst, 1).rstrip()))
            print(sun_line_list)
            # output_data = func_astar(node_dict, start_state, goal_state)
        elif algo == 'UCS':
            node_dict = func_create_node_dict(line_list)
            print(node_dict)
            func_ucs(node_dict, start_state, goal_state)
        else:
            print('The algorithm in the input file is incorrect.')
    if output_data != '':
        func_write_file(output_data)
        func_print_file_content('output.txt')
else:
    print('Something went wrong. Either the file is empty or corrupted.')
