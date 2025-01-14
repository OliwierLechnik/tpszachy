from Node import Node
import math
class DrawableNode(Node):

    def clear(self):
        def helper():
            self.drawn = False
            for n in self.nodes:
                if n is not None:
                    n.clear()

        if not hasattr(self, 'drawn'):
            helper()
            return None

        if self.drawn:
            helper()


    def draw(self):
        if not hasattr(self,"pos"):
            raise Exception("No attribute Node.pos. Call Node.setpos(radius, margin, x, y) first.")
        x,y = self.pos
        colors = [
            (125,125,125),
            (255,0,0),
            (0,255,255),
            (0,0,255),
            (255,255,0),
            (0,255,255),
            (255,0,255)
        ]
        color = colors[self.color]
        self.drawn = True

    def drawNodes(self):
        if not hasattr(self, 'drawn'):
            raise Exception("No attribute `self.drawn`. Did you forget to call `self.clear()` first?")

        if not self.drawn:
            self.draw()
            for i, n in enumerate(self.nodes):
                if n is not None:
                    n.drawNodes()

    def setpos(self, radius, margin, x, y):
        if not hasattr(self, 'pos'):
            self.pos = (x,y)
            for i, n in enumerate(self.nodes):
                if n is not None:
                    n.setpos(
                        radius,
                        margin,
                        x + (2 * radius + margin) * math.cos(i / 3 * math.pi),  # next x
                        y + (2 * radius + margin) * math.sin(i / 3 * math.pi)  # next y
                    )