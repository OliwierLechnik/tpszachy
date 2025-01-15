import os

import pygame
import math

from pygame.examples.moveit import HEIGHT, WIDTH

from shared.Board import Board
from DrawableNode import DrawableNode



class GameGui:
    def __init__(self, players, mycolor, board: Board):

        # Initialize Pygame
        pygame.font.init()
        text_font = pygame.font.SysFont(None, 30)
        pygame.init()

        #sound setup
        pygame.mixer.init()
        path = os.path.join("SoundEffects", "castle.wav")
        self.moveSound = pygame.mixer.Sound(path)
        path = os.path.join("SoundEffects", "Vine_Boom.wav")
        self.VineBoom = pygame.mixer.Sound(path)

        #avatar setup
        path = os.path.join("SoundEffects", "UserAvatar.png")
        self.Avatar = pygame.image.load(path)
        self.Avatar = pygame.transform.scale(self.Avatar, (70, 70))

        # Screen setup
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("asian chess")

        # initializing the board
        board.origin.setpos(15, 5, WIDTH//2, HEIGHT//2)
        board.killAllOrphans()

        self.turn = 1

        self.board = board
        self.screen = screen
        self.font = text_font
        self.mycolor = mycolor

        self.MousePressed = False
        self.CircleAttached = False
        self.target = None
        self.original_x, self.original_y = None, None
        self.running = True

    def draw_text(self, text, text_col, x, y):
        img = self.font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def get_circles_under_pointer(self, mx, my):
        return [node for node in self.board.nodeList if node.isPointInBounds(mx, my)]


    def setTurn(self, turn):
        self.turn = turn

    def CurrentColor(self):
        colors = [
            (191, 191, 191),
            (254, 126, 170),
            (157, 214, 231),
            (248, 230, 189),
            (184, 213, 154),
            (185, 135, 165),
            (195, 13, 119)
        ]
        return colors[self.turn]

    def handleEvent(self):
        msg = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("down")
                MousePressed = True
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if not self.CircleAttached:
                    for node in self.board.nodeList:
                        if node.isPointInBounds(mouse_x, mouse_y) and node.color == self.mycolor and self.mycolor == self.turn:
                            print("dupa", self.mycolor, " ", node.color)
                            self.target = node
                            self.original_x, self.original_y = self.target.pos
                            self.CircleAttached = True
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                nodes = self.get_circles_under_pointer(*pygame.mouse.get_pos())
                if len(nodes) > 1 and Board.validMove(*nodes, self.mycolor):
                    nodes[0].color, nodes[1].color = nodes[1].color, nodes[0].color
                    move = (nodes[0].id, nodes[1].id)
                    msg = f"{nodes[0].id}:{nodes[1].id}"
                    self.moveSound.play()





                if self.target != None:
                    self.target.pos = (self.original_x, self.original_y)
                self.MousePressed = False
                self.target = None
                self.CircleAttached = False
        return msg

    def guiLogic(self):
        if (self.CircleAttached):
            self.target.pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    def loop(self):
        while self.running:
            self.handleEvent()

            self.guiLogic()

            self.render()

    def __del__(self):

        pygame.quit()

    def render(self):
        self.screen.fill((255, 250, 250))  # Clear screen with white color



        # Draw turn info
        self.draw_text("Current Turn", self.CurrentColor(), 50, 50)
        self.draw_text("Your Colour ", self.mycolor, 50, 80)

        for node in self.board.nodeList:
            if node.color != self.mycolor:
                node.draw(self.screen)

        for node in self.board.nodeList:
            if node.color == self.mycolor:
                node.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    board = Board(DrawableNode)
    board.generateBoard()
    board.generatePawns(6)
    gui = GameGui(6, 1, board)
    gui.setTurn(1)
    gui.loop()
