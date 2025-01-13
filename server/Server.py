import asyncio
from Game import Game
import uuid

class Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.unpaired_clients = dict()

    async def handle_client(self, reader, writer):
        client = (reader, writer)
        my_id = str(uuid.uuid4())
        self.unpaired_clients[my_id] = client
        writer.write(b"Connected to the server.\n Type `LIST` to list all open lobbys.\n Type `GET_ID` to get your connmection id.\n Type 'CREATE:<lobby_size>' host a lobby o size <lobby_size>.\n Type `JOIN:<lobby_id>` join open lobby.\n")
        await writer.drain()

        try:
            while True:
                if my_id not in self.unpaired_clients.keys():
                    return
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode().strip()
                if message.startswith("CREATE:"):
                    try:
                        if number := int(message[7:]) in [2,3,4,6]:
                            Game([my_id, reader, writer], number)
                            print("transferred ownership of client to the game thread, exiting the handling thread")
                            return
                        else:
                            writer.write(b"Invalid lobby size.\n")
                    except ValueError as e:
                        writer.write(b"NaN\n")
                elif message.startswith("JOIN:"):
                    print("attenpted join")
                    id = None
                    try:
                        id = uuid.UUID(message[5:])
                    except:
                        writer.write(b"Invalid id format.\n")
                        break
                    if id in Game.game_queue.keys():
                        print("if worked")
                        try:
                            Game.game_queue.get(id).join([my_id,reader,writer])
                            writer.write(b"Joined.\n")
                            await writer.drain()
                            return
                        except KeyError as e:
                            writer.write(b"Failed to join.\n")
                    else:
                        writer.write(b"No game with this id.\n")

                elif message.startswith("LIST"):
                    writer.write(bytes("[" + ",".join(map(str, Game.game_queue.keys())) + "]\n", "utf-8"))

                else:
                    writer.write(b"Unknown command.\n")
                await writer.drain()
        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass
        finally:
            try:
                self.unpaired_clients.pop(my_id)
            except KeyError as e:
                pass





    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()
