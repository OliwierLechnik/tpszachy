import asyncio
import uuid
import time
from board import Board

class Game:

    game_queue = dict()
    def __init__(self, host, size=6):
        self.players = [host]
        self.size = size
        self.uuid = uuid.uuid4()
        self.b = Board()
        Game.game_queue[self.uuid] = self

        asyncio.create_task(self.start())


    def join(self, player):
        for p in self.players:
            p[2].write(bytes(f"[{player[0]} joined the lobby] \n", "utf-8"))
        self.players.append(player)


    async def start(self):
        for p in self.players:
           p[2].write(b"Game Started.\n")
           await p[2].drain()

        while True:
            for p in self.players:
                msg = str()
                try:
                    data = await asyncio.wait_for(p[1].read(100), timeout=0.1)
                    if data:
                        msg: str = data.decode().strip()

                except asyncio.TimeoutError:
                    # If no data is available, skip and do other tasks
                    pass
                except Exception as e:
                    print(f"Error: {e}")

                if msg.startswith("NICK:"):
                    p[0] = msg[5:]

                elif msg:
                   for r in self.players:
                       if r != p:
                           r[2].write(bytes(f"<{p[0]}> {msg}\n", "utf-8"))
                # time.sleep(1)


