import asyncio
class Player:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.timeout = 0.01

    async def applyMsg(self, msg):
        self.writer.write(bytes(msg, "utf-8"))
        await self.writer.drain()

    async def getMsg(self):
        try:
            # Use asyncio.wait_for to set a timeout for the read operation
            data = await asyncio.wait_for(self.reader.read(100), timeout=self.timeout)  # Convert ms to seconds
            print(f"read data={data.decode().strip()}")
            return data.decode().strip()
        except asyncio.TimeoutError:
            return None
