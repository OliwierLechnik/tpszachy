import json

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

def validMove(a,b):
    if a in b:
        return True
    elif a in [b[i][i] for i in range(6) if b[i] is not None and b[i].color != 0]:
        return True
    else:
        return False