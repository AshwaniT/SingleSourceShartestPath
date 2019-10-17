import traceback
import datetime

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Node:
    def __init__(self, node_name):
        self.node_name = node_name
        self.paths = {}
        self.is_visited = False
        self.predecessor_node = None
        self.predecessor_node_wt = 0

    def __str__(self):
        n_str = self.node_name+"->"
        for k, v in self.paths.items():
            n_str=n_str+"("+k.node_name+","+str(v)+"),"
        if self.predecessor_node is not None:
            n_str=n_str+"--->"+self.predecessor_node.node_name+"<<>>"+str(self.predecessor_node_wt)
        return n_str

def file_reader():
    node_dist = {}
    file = None
    try:
        file = open("inputPS3.txt", "r")
        file_lines = file.readlines()
        for line in file_lines:
            token = line.split("/")
            if len(token) == 3:
                node1 = get_node(node_dist, token[0].strip())
                node2 = get_node(node_dist, token[1].strip())
                wt = float(token[2].strip())
                node1.paths[node2] = wt
                node2.paths[node1] = wt
            else:
                token = line.split(":")
                if "DC Node" == token[0].strip():
                    node_dist["startNode"] = node_dist[token[1].strip()]
                elif "WH Node" == token[0].strip():
                    node_dist["endNode"] = node_dist[token[1].strip()]
    except Exception:
        print("error occured in reading file.")
        traceback.print_exc()
    finally:
        if file is not None:
            file.close()
            return node_dist

def get_node(node_dist, node_name):
    if node_name in node_dist:
        return node_dist[node_name]
    node = Node(node_name)
    node_dist[node_name] = node
    return node

def find_shortest_path(start_node):
    q = Queue()
    q.enqueue(start_node)
    while not q.isEmpty():
        node = q.dequeue()
        if node.is_visited:
            continue
        node.is_visited = True
        for next_node, wt in node.paths.items():
            if next_node.is_visited:
                continue
            updated_wt = node.predecessor_node_wt + wt
            if next_node.predecessor_node is None:
                next_node.predecessor_node = node
                next_node.predecessor_node_wt = updated_wt
            elif next_node.predecessor_node_wt > updated_wt:
                next_node.predecessor_node = node
                next_node.predecessor_node_wt = node.predecessor_node_wt + wt
            q.enqueue(next_node)

def print_shortest_path(end_node):
    node_path = end_node
    while node_path is not None:
        print(node_path)
        node_path = node_path.predecessor_node

def print_output(start_node, end_node):
    path = list()
    node_path = end_node
    while node_path is not None:
        path.append(node_path.node_name)
        node_path = node_path.predecessor_node
    path.reverse()
    file = None
    try:
        file = open("outputPS3.txt.", "w")
        truck_speed = 60
        output_line_1 = "Shortest route from DC '{}' to reach Warehouse '{}' is [{}]"
        output_line_2 = "and it has minimum travel distance {} km"
        output_line_3 = "it will take him {} minutes to reach"
        output_line_4 = "Expected arrival time at the warehouse is {}"

        output_line_1 = output_line_1.format(start_node.node_name, end_node.node_name, " ".join(path))
        output_line_2 = output_line_2.format(end_node.predecessor_node_wt)
        total_time_in_minutes = end_node.predecessor_node_wt * 60 / truck_speed
        output_line_3 = output_line_3.format(total_time_in_minutes)
        start_time = datetime.datetime.now()
        start_time = datetime.datetime(hour=10, minute=00, year=start_time.year, month=start_time.month,
                                       day=start_time.day)
        end_time = start_time + datetime.timedelta(minutes=total_time_in_minutes)
        output_line_4 = output_line_4.format(end_time.strftime("%I:%M %p"))

        file.write(output_line_1 + "\n")
        file.write(output_line_2 + "\n")
        file.write(output_line_3 + "\n")
        file.write(output_line_4 + "\n")

        print(output_line_1)
        print(output_line_2)
        print(output_line_3)
        print(output_line_4)

    except Exception:
        print("error occured in writing file.")
    finally:
        if file is not None:
            file.close()

def main():
    node_dist = file_reader()
    start_node = node_dist["startNode"]
    find_shortest_path(start_node)
    end_node = node_dist["endNode"]
    print_output(start_node, end_node)
if __name__ == '__main__':
    main()
