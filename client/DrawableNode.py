import pygame

from shared.Node import Node
import math
class DrawableNode(Node):

    def isPointInBounds(self, mouse_x, mouse_y):
        if not hasattr(self,"pos"):
            raise Exception("DrawableNode must have a pos attribute. u need to call setpos first")
        if not hasattr(self, "radius"):
            raise Exception("DrawableNode must have a radius attribute. U need to call setpos first")
        distance = math.sqrt((mouse_x - self.pos[0]) ** 2 + (mouse_y - self.pos[1]) ** 2)
        return distance <= self.radius


    def draw(self,screen, coloured = True):
        colors = [
            (69,69,69),
            (255,0,0),
            (0,255,0),
            (0,0,255),
            (255,255,0),
            (0,255,255),
            (255,0,255)
        ]
        color = colors[self.color]
        pygame.draw.circle(screen, color, self.pos, self.radius)


    def setpos(self, radius, margin, x, y):
        if not hasattr(self, 'pos'):
            self.pos = (x, y)
            self.radius = radius
            for i, n in enumerate(self.nodes):
                if n is not None:
                    n.setpos(
                        radius,
                        margin,
                        x + (2 * radius + margin) * math.cos(i / 3 * math.pi),  # next x
                        y + (2 * radius + margin) * math.sin(i / 3 * math.pi)  # next y
                    )