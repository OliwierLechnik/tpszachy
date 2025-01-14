import json

class Node:

    def __init__(self):
        self.nodes = [
            None,  # 0 - right
            None,  # 1 - bottom right
            None,  # 2 - bottom left
            None,  # 3 - left
            None,  # 4 - top left
            None   # 5 - top right
        ]
        self.color = 0


    def setColor(self, color):
        self.color = color


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

    def to_json(self):
        # Serialize node as a dictionary
        return {
            "color": self.color,
            "nodes": [node.to_json() for node in self.nodes if node is not None and node is not self]
        }

    @classmethod
    def from_json(cls, data, node_map):
        # Create a new node and populate its data
        node = cls()
        node.color = data["color"]
        node.nodes = [node_map[node_id] if node_id else None for node_id in data["nodes"]]
        return node