import os
import time

import pygame
import math

from pygame.examples.moveit import HEIGHT, WIDTH

from Board import Board
from DrawableNode import DrawableNode



class GameGui:
    def __init__(self, players, mycolor, board: Board):

        # Initialize font
        pygame.font.init()
        text_font = pygame.font.SysFont(None, 30)
        pygame.init()

        #sound setup
        self.LoadEmotes()
        self.LoadSounds()



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

        self.activeEmote = None
        self.activeSound = None
        self.activeEmoteOp = 0

    def LoadEmotes(self):

        path = os.path.join("client/EmoteFiles", "Hu_Tao.png")
        self.Tao = pygame.transform.scale(pygame.image.load(path), (400, 400))

        path = os.path.join("client/EmoteFiles", "Skull.png")
        self.Skull = pygame.transform.scale(pygame.image.load(path), (400, 400))

        path = os.path.join("client/EmoteFiles", "headEmpty.png")
        self.HeadEmpty = pygame.transform.scale(pygame.image.load(path), (400, 400))

        path = os.path.join("client/EmoteFiles", "QiqiFall.png")
        self.Qiqi = pygame.transform.scale(pygame.image.load(path), (400, 400))

        path = os.path.join("client/EmoteFiles", "Megamind.png")
        self.Megamind = pygame.transform.scale(pygame.image.load(path), (400, 400))

        path = os.path.join("client/EmoteFiles", "cringe.png")
        self.Cringe = pygame.transform.scale(pygame.image.load(path), (400, 400))

        path = os.path.join("client/EmoteFiles", "autismo.png")
        self.Autismo = pygame.transform.scale(pygame.image.load(path), (400, 400))

        path = os.path.join("client/EmoteFiles", "DeepFry.png")
        self.DeepFry = pygame.transform.scale(pygame.image.load(path), (400, 400))

    def LoadSounds(self):
        pygame.mixer.init()

        self.MoveSound = pygame.mixer.Sound(os.path.join("client/EmoteFiles", "castle.wav"))
        self.VineBoom = pygame.mixer.Sound(os.path.join("client/EmoteFiles", "Vine_Boom.wav"))
        self.Akira = pygame.mixer.Sound(os.path.join("client/EmoteFiles", "Akira.wav"))
        self.Ping = pygame.mixer.Sound(os.path.join("client/EmoteFiles", "Ping.wav"))
        self.YodaDeath = pygame.mixer.Sound(os.path.join("client/EmoteFiles", "YodaDeath.wav"))
        self.Boom = pygame.mixer.Sound(os.path.join("client/EmoteFiles", "Boom.wav"))

    def getEmote(self, EmoteID):
        EmoteID = EmoteID - 1   # tutaj jest -1 bo do getEmote wrzucam to jaki przycisk był kliknięty a nie od razu id emotki
        Emotes = [
            (self.Tao, self.VineBoom),
            (self.Skull, self.Akira),
            (self.HeadEmpty, self.Ping),
            (self.Qiqi, self.YodaDeath),
            (self.Megamind, self.Boom),
            (self.Cringe, self.Akira),
            (self.Autismo, self.Akira),
            (self.DeepFry, self.Akira),
            (self.HeadEmpty, self.Akira)

        ]
        return Emotes[EmoteID]

    def setActiveEmote(self,EmoteID):
        self.activeEmote = self.getEmote(EmoteID)[0]
        self.activeSound = self.getEmote(EmoteID)[1]
        self.activeEmoteOp = 350

    def playEmote(self):

        if self.activeEmoteOp == 350:
            pygame.mixer.Sound.play(self.activeSound)

        self.activeEmote.set_alpha(255 if self.activeEmoteOp > 255 else self.activeEmoteOp)
        self.screen.blit(self.activeEmote, (200, 100))
        self.activeEmoteOp = self.activeEmoteOp  - 1

        if self.activeEmoteOp  == 0:
            self.activeEmote, self.activeSound = None, None




    def draw_text(self, text, text_col, x, y):
        img = self.font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def get_circles_under_pointer(self, mx, my):
        return [node for node in self.board.nodeList if node.isPointInBounds(mx, my)]


    def setTurn(self, turn):
        self.turn = turn

    def CurrentColor(self, ColorID):
        colors = [
            (191, 191, 191),
            (254, 126, 170),
            (157, 214, 231),
            (248, 230, 189),
            (184, 213, 154),
            (185, 135, 165),
            (195, 13, 119)
        ]
        return colors[ColorID]

    def handleEvent(self):
        msg = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYUP:

                if event.key - 48 > 0 and event.key - 48 < 10:
                    msg = f"EMOTE:{event.key - 48}"
                    # self.setActiveEmote(event.key - 48)

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
                    # nodes[0].color, nodes[1].color = nodes[1].color, nodes[0].color
                    # move = (nodes[0].id, nodes[1].id)
                    msg = f"MOVE:{nodes[0].id};{nodes[1].id}"
                    self.MoveSound.play()


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
        self.screen.fill((82, 81, 80))  # Clear screen with white color

        # Draw turn info
        self.draw_text("Current Turn", self.CurrentColor(self.turn), 50, 50)
        self.draw_text("Your Colour ", self.CurrentColor(self.mycolor), 50, 80)


        for node in self.board.nodeList:
            if node.color != self.mycolor:
                node.draw(self.screen)

        for node in self.board.nodeList:
            if node.color == self.mycolor:
                node.draw(self.screen)

        if self.activeEmoteOp != 0:
            self.playEmote()

        pygame.display.flip()


if __name__ == "__main__":
    board = Board(DrawableNode)
    board.generateBoard()
    board.generatePawns(6)
    gui = GameGui(6, 1, board)
    gui.setTurn(1)
    gui.loop()
