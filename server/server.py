import asyncio
from game import Game
from mmh3 import hash

class Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.unpaired_clients = dict()
        self.pairing_requests = set()

    async def handle_client(self, reader, writer):
        client = (reader, writer)
        my_hash = f"{hash(f'{client[0]}:{client[1]}') & 0xFFFFFFFF:08x}"
        self.unpaired_clients[my_hash] = client
        writer.write(b"Connected to the server.\n Type `LIST` to list all connections waiting for pairing request.\n Type `GET_ID` to get your connmection id.\n Type 'PAIR:<client_id>' to send a pairing request.\n Type `ACCEPT:<client_id>` to accept a pairing request.\n")
        writer.write(bytes(",".join([key for key in self.unpaired_clients.keys() if key != my_hash] or ["Wow so empty"]) + "\n", "utf-8"))
        await writer.drain()

        try:
            while True:
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode().strip()
                if message.startswith("PAIR:"):
                    await self.pairing_requests.add((my_hash, message[5:]))
                elif message.startswith("ACCEPT:"):
                    writer.write(bytes("[" + " ".join([key for key in self.unpaired_clients.keys() if key != my_hash] or ["Wow so empty"]) + "]\n", "utf-8"))
                elif message.startswith("GET_ID"):
                    writer.write(bytes(my_hash, "utf-8"))
                elif message.startswith("LIST"):
                    writer.write(bytes(",".join([key for key in self.unpaired_clients.keys() if key != my_hash] or ["Wow so empty"]) + "\n", "utf-8"))
                else:
                    writer.write(b"Unknown command.\n")
                    await writer.drain()
        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass
        finally:
            self.unpaired_clients.pop(my_hash)
            writer.close()
            await writer.wait_closed()

    async def handle_pair_request(self, client, target_id):
        reader, writer = client
        target_client = None

        for candidate_reader, candidate_writer in self.unpaired_clients:
            if id(candidate_writer) == int(target_id):  # Match by unique writer ID
                target_client = (candidate_reader, candidate_writer)
                break

        if not target_client:
            writer.write(b"Target client not found.\n")
            await writer.drain()
            return

        # Send pairing request to the target client
        target_reader, target_writer = target_client
        target_writer.write(b"PAIRING REQUEST RECEIVED. Type 'ACCEPT' to accept.\n")
        await target_writer.drain()

        # Wait for the target client's response
        try:
            response = await asyncio.wait_for(target_reader.read(100), timeout=30)
            if response.decode().strip() == "ACCEPT":
                # Pairing accepted, start the game
                self.unpaired_clients.discard(client)
                self.unpaired_clients.discard(target_client)
                writer.write(b"Pairing successful! Starting the game.\n")
                await writer.drain()
                target_writer.write(b"Pairing successful! Starting the game.\n")
                await target_writer.drain()

                # Transfer ownership of clients to Game
                game = Game(client, target_client)
                asyncio.create_task(game.start())
            else:
                writer.write(b"Pairing request denied.\n")
                await writer.drain()
        except asyncio.TimeoutError:
            writer.write(b"Pairing request timed out.\n")
            await writer.drain()

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()
