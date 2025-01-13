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