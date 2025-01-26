import json

from Node import Node
import numpy as np
from random import Random

class Board:
    def __init__(self, nodeImplementation = Node):
        self.nodeImplementation = nodeImplementation

    def generateBoard(self):
        amounts = [1,2,3,4,13,12,11,10,9,10,11,12,13,4,3,2,1]
        rawBoard = np.zeros((17, 27), object)
        nodeList = list()
        odd = False
        for i, a in enumerate(amounts):
            for j in range(a // 2 + 1):
                try:
                    node_a = rawBoard[i, 12 + (2 * j - (1 if odd else 0))] = self.nodeImplementation()
                    nodeList.append(node_a)

                    if 12 + (2 * j - (1 if odd else 0)) != 12 - (2 * j - (1 if odd else 0)):
                        node_b = rawBoard[i, 12 - (2 * j - (1 if odd else 0))] = self.nodeImplementation()
                        nodeList.append(node_b)
                except:
                    print(f"debil ({i},{j})")


            odd = not odd

        for i in range(16):
            for j in range(27):
                toAdd = {
                    0: (i,j+2),
                    1: (i+1, j + 1),
                    2: (i + 1, j - 1),
                    3: (i, j - 2),
                    4: (i-1, j - 1),
                    5: (i - 1, j + 1)
                }
                if rawBoard[i,j] != 0:
                    if not i > 0:  # top doesnt exists
                        toAdd.pop(4, None)
                        toAdd.pop(5, None)
                    if not i < 16:  # bottom doesnt exists
                        toAdd.pop(1, None)
                        toAdd.pop(2, None)
                    if not j > 0:  # left doesnt exists
                        toAdd.pop(2, None)
                        toAdd.pop(3, None)
                        toAdd.pop(4, None)
                    if not j < 25:  # right doesnt exists
                        toAdd.pop(0, None)
                        toAdd.pop(1, None)
                        toAdd.pop(5, None)
                    for k, v in toAdd.items():
                        if n := rawBoard[v[0], v[1]]:
                            n.on_graph = True
                            rawBoard[i,j][k] = n
        self.rawBoard = rawBoard
        self.origin = rawBoard[8,12]
        self.nodeList = nodeList
        self.killAllOrphans()

    def killAllOrphans(self):  # requires to use setpos first
        self.nodeList = [node for node in self.nodeList if node.on_graph]

    def generatePawns(self, n):  # n - number of players
        if n not in [2,3,4,6]:
            raise ValueError(f"Invalid amount of players ({n}) passed to the Board.generatePawns(n).")

        def add_c_6(n):
            return (6+n)%6

        translator = {
            2: (2,5),
            3: (0, 2, 4),
            4: (0, 1, 3, 4),
            6: (0, 1, 2, 3, 4, 5)
        }

        for c in translator[n]:
            d = add_c_6(c-1)
            colorOrigin = self.origin[c][c][c][d][d][d]
            colorOrigin.setColor(c+1)

            for i in [0,2,4]:
                colorOrigin[add_c_6(c+i)][add_c_6(d+i)].setColor(c+1)

            for node in colorOrigin.nodes:
                node.setColor(c+1)


    def generatePawnsRandom(self, n):
        Random.seed(69420)
        colors = {
            2: (2, 5),
            3: (0, 2, 4),
            4: (0, 1, 3, 4),
            6: (0, 1, 2, 3, 4, 5)
        }[n]
        for c in colors:
            for _ in range(10):
                node = Random.choice(self.nodeList)
                while (node := Random.choice(self.nodeList)).color != 0:
                    node.color = c+1




    def printBoard(self):
        for i in range(17):
            for j in range(25):
                print(' ' if self.rawBoard[i,j] == 0 else f"{self.rawBoard[i,j].color}", end='')
            print('')
    @staticmethod
    def validMove(a, b, turn):
        print(f"Valid Move {a.color} {b.color} {turn}")
        if 0 not in [a.color, b.color]:
            return False
        if b.color == 0:
            a, b = b, a
        if b.color != turn:
            return False
        if a in [n for n in b if n is not None and n.color == 0]:
            return True
        elif a in [b[i][i] for i in range(6) if
                   b[i] is not None and b[i].color != 0 and b[i][i] is not None and b[i][i].color == 0]:
            return True
        else:
            return False

    def getNodesByIDs(self, ids):
        return [n for n in self.nodeList if n.id in ids]

if __name__ == "__main__":
    b = Board()
    b.generateBoard()
    b.generatePawns(3)
    b.printBoard()
    print(b.origin.__class__)

    def diff():
        pass

    def patch():
        pass

    def toJson(self):
        pass

    def fromJson(self):
        pass