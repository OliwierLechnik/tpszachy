import socket
import threading
import sys

from server.DatabaseCommands import DataBase


import select
from shared.Board import Board
from client.DrawableNode import DrawableNode
from client.GameGUI import GameGui


def actuallGameLoop(players=6):
    Db = DataBase()

    board = Board(DrawableNode)
    board.generateBoard()
    board.generatePawns(players)

    gui = GameGui(players, 2, board)
    gui.setTurn(1)

    print("starting game loop")

    while gui.running:

        Db = DataBase()
        Db.getGameFromDB("1a6004ef-d2ab-4abb-b94e-d029c11e96c6")
        MoveList = Db.cursor.fetchall()
        for each in MoveList:

            Move = MoveList[each][0][0]
            k, v = Move.split(":")
            if k == "MOVE":
                a, b = board.getNodesByIDs((int(v.split(";")[0]), int(v.split(";")[1])))
                a.color, b.color = b.color, a.color

        gui.guiLogic()

        gui.render()

    print("exiting game")


actuallGameLoop()