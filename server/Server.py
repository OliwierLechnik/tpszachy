import asyncio
from ServerCommandHandler import CreateCommandHandler, JoinCommandHandler, ListCommandHandler, UnknownCommandHandler
class Server:
    _instance = None  # Class-level attribute to hold the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Server, cls).__new__(cls)
        return cls._instance

    def __init__(self, host='127.0.0.1', port=8888):
        if not hasattr(self, 'initialized'):
            self.host = host
            self.port = port
            self.initialized = True  # Avoid reinitializing in subsequent calls

            # Set up the chain of responsibility
            self.command_handler = CreateCommandHandler(
                JoinCommandHandler(
                    ListCommandHandler(
                        UnknownCommandHandler()
                    )
                )
            )

    async def handle_client(self, reader, writer):
        print("New client connected")
        client = (reader, writer)
        writer.write(b"Connected to the server.\n"
                     b"Type `LIST` to list all open lobbies.\n"
                     b"Type `GET_ID` to get your connection ID.\n"
                     b"Type 'CREATE:<lobby_size>' to host a lobby of size <lobby_size>.\n"
                     b"Type `JOIN:<lobby_id>` to join an open lobby.\n")
        await writer.drain()

        pauser = asyncio.Event()

        try:
            while True:

                data = await reader.read(100)
                if not data:
                    break

                message = data.decode().strip()
                context = {
                    'reader': reader,
                    'writer': writer
                }
                pauser.clear()
                pauser.wait()
                msg = await self.command_handler.handle(message, context)
                pauser.set()
                if msg in ["JOINED", "CREATED"]:
                    print(msg)
                    return

        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass

        finally:# Log the disconnection
            print(f"Client disconnected.")
            # writer.close()
            # await writer.wait_closed()

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

# Usage example
if __name__ == "__main__":
    server = Server(host='127.0.0.1', port=42069)
    asyncio.run(server.start())

