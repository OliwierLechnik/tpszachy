import asyncio

class Game:

    gameList = set()

    def __init__(self, client1, client2):
        self.client1 = client1
        self.client2 = client2
        Game.gameList.append(self)
        self.start()

    async def start(self):
        print("Game started between two clients.")
        reader1, writer1 = self.client1
        reader2, writer2 = self.client2

        try:
            while True:
                await self.exchange_messages(reader1, writer1, reader2, writer2)
                await self.exchange_messages(reader2, writer2, reader1, writer1)
        except (asyncio.IncompleteReadError, ConnectionResetError):
            print("A client disconnected.")
        finally:
            writer1.close()
            writer2.close()
            await writer1.wait_closed()
            await writer2.wait_closed()
            print("Game ended.")

    async def exchange_messages(self, reader, writer, opponent_reader, opponent_writer):
        writer.write(b"Your turn: ")
        await writer.drain()
        data = await reader.read(100)
        if not data:
            raise ConnectionResetError
        opponent_writer.write(b"Opponent says: " + data)
        await opponent_writer.drain()
