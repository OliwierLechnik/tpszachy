from collections import deque
import random

from Board import Board


class Bot:
    def __init__(self, board):
        pass
        # self.turn = 1
        # self.mycolor = mycolor
        self.board = board

    def setTurn(self, turn):
        self.turn = turn


        return -1

    def get_nodes_with_preferred_color(self):
        """
        Finds all nodes on the board where `preferred_color` equals `self.mycolor`
        and the node's color is 0 (empty).

        Returns:
            List[Node]: A list of target nodes that match the criteria.
        """
        return [
            node for node in self.board.getList()
            if node.preffered_color == self.mycolor
        ]
    def get_my_nodes(self):
        """
        Finds all nodes on the board where `preferred_color` equals `self.mycolor`
        and the node's color is 0 (empty).

        Returns:
            List[Node]: A list of target nodes that match the criteria.
        """
        return [
            node for node in self.board.getList()
            if node.color == self.mycolor
        ]

    async def applyMsg(self, response):
        if response is None:
            return None
        if response.startswith("MOVE:"):
            print("X")
            k, v = response.split(":")
            print(f"BOT X: k={k} v={v}")
            p,q, r = v.split(";")
            # print(f"BOT: {p} {q}")
            # nodes = self.board.getNodesByIDs([int(p), int(q)])
            # print(f"XXX: {nodes}")
            # a.color, b.color = b.color, a.color
            # print("XXXX")
            self.setTurn(int(r))
            print("BOT Applied move")
        elif response.startswith("Game Started:"):

            _, players, mycolor, turncolor = response.split(":")
            print(players, mycolor, turncolor)
            self.turn = int(turncolor)
            self.mycolor = int(mycolor)

            print(f"BOT setting turn={turncolor}, mycolor={mycolor}, board=Board({players})")



    async def getMsg(self):
        if self.mycolor == self.turn:
            print("BOT: my turn")
        else:
            return Non

        my_nodes = self.get_my_nodes()
        node = random.choice(my_nodes)
        while not node.has_empty_neightbors():
            node = random.choice(my_nodes)

        targets = self.get_nodes_with_preferred_color()

        target = targets[0]
        l = node.metric(target)
        for t in targets:
            if (l1 := node.metric(t)) < l:
                target = t
                l = l1

        candidate_moves = [n for n in node if n and n.color == 0]
        for i in range(6):
            if node[i] and node[i].color != 0 and node[i][i] and node[i][i].color == 0:
                candidate_moves.append(node[i][i])


        move = candidate_moves[0]
        l = move.metric(target)
        for n in candidate_moves:
            if (l1 := n.metric(target)) < l:
                move = n
                l = l1

        return f"MOVE:{node.id};{move.id}"

