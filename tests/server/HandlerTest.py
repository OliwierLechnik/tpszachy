import sys

sys.path.append('../../server')

import unittest
from unittest.mock import AsyncMock, Mock
from ServerCommandHandler import CreateCommandHandler, JoinCommandHandler, ListCommandHandler, UnknownCommandHandler

class TestCommandHandlers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock context with a writer
        self.writer = AsyncMock()
        self.context = {
            'reader': AsyncMock(),
            'writer': self.writer
        }

    async def test_create_command_handler_valid(self):
        handler = CreateCommandHandler()
        command = "CREATE:4"
        await handler.handle(command, self.context)

        # Check if the writer writes the correct response
        self.writer.write.assert_called_with(b"Game Lobby Started.\n")
        self.writer.drain.assert_awaited()

    async def test_create_command_handler_invalid_size(self):
        handler = CreateCommandHandler()
        command = "CREATE:5"  # Invalid size
        await handler.handle(command, self.context)

        self.writer.write.assert_called_with(b"Invalid lobby size.\n")
        self.writer.drain.assert_awaited()

    async def test_join_command_handler_valid(self):
        # Mock a valid game queue entry
        from Game import Game
        Game.game_queue = {Mock(): Mock()}  # Mock game queue with a valid UUID

        handler = JoinCommandHandler()
        command = f"JOIN:{list(Game.game_queue.keys())[0]}"
        await handler.handle(command, self.context)

        # Check if the writer writes the correct response
        self.writer.write.assert_called_with(b"Joined.\n")
        self.writer.drain.assert_awaited()

    async def test_list_command_handler(self):
        # Mock the game queue keys
        from Game import Game
        Game.game_queue = {Mock(): Mock(), Mock(): Mock()}

        handler = ListCommandHandler()
        command = "LIST"
        await handler.handle(command, self.context)

        # Check if the writer writes the correct response
        expected_response = bytes(
            "[" + ",".join(map(str, Game.game_queue.keys())) + "]\n", "utf-8"
        )
        self.writer.write.assert_called_with(expected_response)
        self.writer.drain.assert_awaited()

    async def test_unknown_command_handler(self):
        handler = UnknownCommandHandler()
        command = "UNKNOWN_COMMAND"
        await handler.handle(command, self.context)

        # Check if the writer writes the correct response
        self.writer.write.assert_called_with(b"Unknown command.\n")
        self.writer.drain.assert_awaited()

    async def test_chain_of_responsibility(self):
        # Chain of responsibility: Create -> Join -> List -> Unknown
        handler = CreateCommandHandler(
            JoinCommandHandler(
                ListCommandHandler(
                    UnknownCommandHandler()
                )
            )
        )

        # Send an unknown command
        command = "INVALID_COMMAND"
        await handler.handle(command, self.context)

        # Check if the UnknownCommandHandler is reached
        self.writer.write.assert_called_with(b"Unknown command.\n")
        self.writer.drain.assert_awaited()

