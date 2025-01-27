import json
from collections import deque

class Node:

    id_counter = 0
    def __init__(self):
        self.nodes = [
            None,  # 0 - right
            None,  # 1 - bottom right
            None,  # 2 - bottom left
            None,  # 3 - left
            None,  # 4 - top left
            None   # 5 - top right
        ]
        self.id = Node.id_counter
        Node.id_counter += 1

        self.color = 0
        self.preffered_color = None
        self.on_graph = False


    def setColor(self, color):
        self.color = color

    def setPrefferedColor(self, color):
        self.preffered_color = color

    def has_empty_neightbors(self):
        for n in self.nodes:
            if n and n.color == 0:
                return True
        return False

    def metric(self, end):
        start = self
        """
        Computes the minimal distance between two nodes in the graph.
    
        :param start: The starting Node object.
        :param end: The target Node object.
        :return: The shortest distance (integer) between start and end. 
                 Returns -1 if there's no path between the nodes.
        """
        if start == end:
            return 0

        visited = set()
        queue = deque([(start, 0)])  # (current_node, current_distance)

        while queue:
            current, distance = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            for neighbor in current.nodes:
                if neighbor:  # Ensure the neighbor exists
                    if neighbor == end:
                        return distance + 1
                    queue.append((neighbor, distance + 1))

        # If we exhaust the queue without finding `end`, there's no path
        return -1


    def __getitem__(self, index):
        if index < 0 or index > 5:
            raise IndexError(f"Invalid index: {index}")
        return self.nodes[index]

    def __setitem__(self, index, value):
        if index < 0 or index > 5:
            raise IndexError(f"Invalid index: {index}")
        self.nodes[index] = value

    def __delitem__(self, index):
        self.nodes[index] = None
