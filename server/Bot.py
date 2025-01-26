from collections import deque
from random import random

from shared.Board import Board


class Bot:
    def __init__(self, players, mycolor, board: Board):

        self.turn = 1
        self.mycolor = mycolor
        self.board = board

    def setTurn(self, turn):
        self.turn = turn

    def shortest_path_length(start_node, end_node):

        if start_node == end_node:
            return 0  # If both nodes are the same, no traversal is needed

        visited = set()  # To keep track of visited nodes
        queue = deque([(start_node, 0)])  # Queue of tuples: (current_node, current_distance)

        while queue:
            current_node, distance = queue.popleft()

            if current_node in visited:
                continue

            visited.add(current_node)

            # Check all neighbors
            for neighbor in current_node:
                if neighbor is not None and neighbor.color == 0:  # Only traverse nodes with color 0
                    if neighbor == end_node:
                        return distance + 1  # Found the target node
                    queue.append((neighbor, distance + 1))

        return -1

    def get_nodes_with_preferred_color(self):
        """
        Finds all nodes on the board where `preferred_color` equals `self.mycolor`
        and the node's color is 0 (empty).

        Returns:
            List[Node]: A list of target nodes that match the criteria.
        """
        return [
            node for node in self.board.nodeList
            if node.preferred_color == self.mycolor and node.color == 0
        ]

    def find_closest_target(self, start_node, target_nodes):
        """
        Finds the closest node to `start_node` among the `target_nodes`.

        Args:
            start_node (Node): The node from which the distance is calculated.
            target_nodes (List[Node]): A list of target nodes to consider.

        Returns:
            tuple: (closest_node, shortest_distance) if a valid path exists,
                   (None, float('inf')) if no valid path is found.
        """
        closest_node = None
        shortest_distance = float('inf')

        for target_node in target_nodes:
            distance = self.shortest_path_length(start_node, target_node)
            if distance != -1 and distance < shortest_distance:
                closest_node = target_node
                shortest_distance = distance

        return closest_node, shortest_distance

    async def ApplyMessage(self, response):
        if response is not None:
            print(response)
            k, v = response.split(":")
            if k == "MOVE":
                a, b = self.board.getNodesByIDs((int(v.split(";")[0]), int(v.split(";")[1])))
                a.color, b.color = b.color, a.color
                self.setTurn(int(v.split(";")[2]))
        return None

    def getMessage(self):
        """
        Finds the first move for a node with `self.mycolor` that brings it closer
        to a node with `preferred_color` equal to `self.mycolor`. If no such move
        is found, it randomly moves a pawn to any neighboring empty space.

        Returns:
            str: A message in the format "start_node:end_node" representing the move.
            None: If no valid move is found, and there are no pawns to move.
        """
        target_nodes = self.get_nodes_with_preferred_color()

        # Iterate through all nodes with `self.mycolor`
        for node in self.board.nodeList:
            if node.color == self.mycolor:  # Check if the node has `self.mycolor`
                closest_target, initial_distance = self.find_closest_target(node, target_nodes)

                if closest_target is not None:
                    # Check if moving to any neighbor reduces the distance to the target
                    for neighbor in node:
                        if neighbor is not None and neighbor.color == 0:  # Valid neighbor to move to
                            # Temporarily simulate the move
                            original_color = neighbor.color
                            neighbor.color = self.mycolor
                            node.color = 0

                            _, new_distance = self.find_closest_target(neighbor, target_nodes)

                            # Revert the move
                            neighbor.color = original_color
                            node.color = self.mycolor

                            if new_distance < initial_distance:  # Valid improvement
                                return f"{node.id}:{neighbor.id}"

        # If no valid move found, randomly move a pawn to a neighboring empty space
        available_pawns = [node for node in self.board.nodeList if node.color == self.mycolor]

        for pawn in available_pawns:
            # Get all neighboring nodes that are empty (color == 0)
            empty_neighbors = [neighbor for neighbor in pawn if neighbor is not None and neighbor.color == 0]

            if empty_neighbors:
                # Randomly select an empty neighboring space
                random_empty_space = random.choice(empty_neighbors)

                # Return the move message
                return f"{pawn.id}:{random_empty_space.id}"

        return None  # Return None if no valid move or pawns to move

