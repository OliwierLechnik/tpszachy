import asyncio
import uuid
import time

import threading

from Database.DatabaseCommands import DataBase
from Board import Board

from Player import Player
from Bot import Bot

class Game:

    game_queue = dict()
    def __init__(self, host, size=6, bot=0):
        self.players = [Player(*host)]
        self.size = size
        self.uuid = uuid.uuid4()
        self.b = Board()
        self.b.generateBoard()
        self.b.generatePawns(size)
        for _ in range(bot):
            self.players.append(Bot(self.b))
            print("created a bot")
        self.variant = 1
        Game.game_queue[self.uuid] = self

        self.DB = DataBase()

    async def check_for_start(self):
        if len(self.players) == self.size:
            print("Starting game")
            Game.game_queue.pop(self.uuid)
            await self.start()
    async def join(self, player):
        self.players.append(Player(*player))

        print(f"joined {len(self.players)}/{self.size}")
        if len(self.players) == self.size:
            print("Starting game")
            Game.game_queue.pop(self.uuid)
            await self.start()

    async def start(self):

        colors = [i + 1 for i in {
            2: (2,5),
            3: (0, 2, 4),
            4: (0, 1, 3, 4),
            6: (0, 1, 2, 3, 4, 5)
        }[self.size]]



        turn = 0
        for i, r in enumerate(self.players):
            await r.applyMsg(f"Game Started:{len(self.players)}:{colors[i]}:{colors[turn]}")

        moves = list()

        while True:
            response = await asyncio.gather(
                *[player.getMsg() for player in self.players]
            )

            # print(response)

            for s in response:
                if s and s.startswith("EMOTE:"):
                    for r in self.players:
                        await r.applyMsg(s)

            msg = response[turn]

            if not msg or not msg.startswith("MOVE:"):
                continue

            print(f"received {msg} from {colors[turn]}")

            move = False
            try:
                move = self.b.validMove(
                    *self.b.getNodesByIDs(
                        [int(i) for i in msg[5:].split(";")]
                    ),
                    colors[turn]
                )
            except Exception as e:
                print(f"Exception accured invalid ids, e.what() {e}")

            print(f"move {move}")
            if not move:
                # self.players[turn][2].write(bytes(f"Invalid move.", "utf-8"))
                # await self.players[turn][2].drain()
                continue

            moves.append(msg)

            a, b = self.b.getNodesByIDs(
                        [int(i) for i in msg[5:].split(";")]
                    )
            a.color, b.color = b.color, a.color

            turn = (turn + 1) % self.size

            for r in self.players:
                # add move to the database
                self.DB.addMoveDB(self.uuid, f"{msg};{colors[turn]}")

                await r.applyMsg(f"{msg};{colors[turn]}")

            await asyncio.sleep(0.01)




