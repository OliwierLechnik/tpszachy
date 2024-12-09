import asyncio
from server import Server


# entry point
if __name__ == "__main__":
    server = Server(host='127.0.0.1', port=42069)
    asyncio.run(server.start())
