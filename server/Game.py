import asyncio
import uuid
import time
from shared.Board import Board

class Game:

    game_queue = dict()
    def __init__(self, host, size=6):
        self.players = [host]
        self.size = size
        self.uuid = uuid.uuid4()
        self.b = Board()
        self.b.generateBoard()
        Game.game_queue[self.uuid] = self


    def join(self, player):
        for p in self.players:
            p[2].write(bytes(f"[{player[0]} joined the lobby] \n", "utf-8"))
        self.players.append(player)

        print(f"joined {len(self.players)}/{self.size}")
        if len(self.players) == self.size:
            print("Starting game")
            Game.game_queue.pop(self.uuid)
            asyncio.create_task(self.start())



    async def start(self):

        colors = {
            2: (2,5),
            3: (0, 2, 4),
            4: (0, 1, 3, 4),
            6: (0, 1, 2, 3, 4, 5)
        }[self.size]


        turn = 0
        for i, r in enumerate(self.players):
            p[2].write(b"Game Started.")
            r[2].write(bytes(f"{colors[i]}:{colors[turn]}", "utf-8"))
            await r[2].drain()

        moves = list()

        while True:
            data = self.players[turn][1].read(100)
            msg = data.strip()

            if msg == "End of turn.":
                turn = (turn + 1) % self.size
                for r in self.players:
                    r[2].write(bytes(f"TURN:{colors[turn]}", "utf-8"))
                    await r[2].drain()
                continue


            move = False
            try:
                move = self.b.validMove(
                    *self.b.getNodesByIDs(
                        msg.split(";")
                    ),
                    colors[turn]
                )
            except Exception as e:
                print(f"Exception accured invalid ids, e.what() {e}")

            if not move:
                self.players[turn][2].write(bytes(f"Invalid move.", "utf-8"))
                await self.players[turn][2].drain()
                continue

            moves.append(msg)

            a, b = self.b.getNodesByIDs(msg.split(";"))
            a.color, b.color = b.color, a.color


            for r in self.players:
                r[2].write(bytes(f"MOVE:{msg}", "utf-8"))
                await r[2].drain()



