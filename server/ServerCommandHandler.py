from Game import Game
import asyncio
import uuid

class CommandHandler:
    """Abstract handler in the chain of responsibility pattern."""
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    async def handle(self, command, context):
        if self.next_handler:
            await self.next_handler.handle(command, context)

class CreateCommandHandler(CommandHandler):
    async def handle(self, command, context):
        if command.startswith("CREATE:"):
            try:
                number = int(command[7:])
                if number in [2, 3, 4, 6]:
                    Game([context['reader'], context['writer']], number)
                    context['writer'].write(b"Game Lobby Started.\n")
                    await context['writer'].drain()
                    return  "CREATED"# Command handled, exit chain
                else:
                    context['writer'].write(b"Invalid lobby size.\n")
            except ValueError:
                context['writer'].write(b"NaN\n")
            await context['writer'].drain()
        else:
            await super().handle(command, context)

class JoinCommandHandler(CommandHandler):
    async def handle(self, command, context):
        if command.startswith("JOIN:"):
            try:
                id = uuid.UUID(command[5:])
                if id in Game.game_queue.keys():
                    try:
                        await Game.game_queue.get(id).join([context['reader'], context['writer']])
                        context['writer'].write(b"Joined.\n")
                        await context['writer'].drain()
                        return  "JOINED"# Command handled, exit chain
                    except KeyError:
                        context['writer'].write(b"Failed to join.\n")
                else:
                    context['writer'].write(b"No game with this ID.\n")
            except ValueError:
                context['writer'].write(b"Invalid ID format.\n")
            await context['writer'].drain()
        else:
            await super().handle(command, context)

class ListCommandHandler(CommandHandler):
    async def handle(self, command, context):
        if command.startswith("LIST"):
            context['writer'].write(bytes("[" + ",".join(map(str, Game.game_queue.keys())) + "]\n", "utf-8"))
            await context['writer'].drain()
        else:
            await super().handle(command, context)

class UnknownCommandHandler(CommandHandler):
    async def handle(self, command, context):
        context['writer'].write(b"Unknown command.\n")
        await context['writer'].drain()
