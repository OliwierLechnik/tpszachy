import pygame
import math

from shared.Board import Board
from DrawableNode import DrawableNode

def validMove(a,b):
    if a in b:
        return True
    elif a in [b[i][i] for i in range(6) if b[i] is not None and b[i].color != 0]:
        return True
    else:
        return False

# Function to check if a point is inside a circle
def is_point_in_circle(x, y, cx, cy, radius):
    distance = math.sqrt((x - cx)**2 + (y - cy)**2)
    return distance <= radius

pygame.font.init()
text_font = pygame.font.SysFont(None, 30)

def draw_text(text, font, text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("asian chess")
# Circle properties
circle_x2, circle_y2 = 111, 111  # Circle center
circle_radius = 20

#initializing the board
b = Board(DrawableNode)
b.generateBoard()
b.generatePawns(6)
b.origin.setpos(15, 5, 400, 300)
b.killAllOrphans()

Mycolor = 2
MyTurn = True



MousePressed = False
CircleAttached = False
target = None
original_x, original_y = None, None

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                MyTurn = False

        elif event.type == pygame.MOUSEBUTTONDOWN and MyTurn:
            MousePressed = True
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if not CircleAttached:
                for node in b.nodeList:
                    if node.isPointInBounds(mouse_x, mouse_y):
                        target = node
                        original_x, original_y = target.pos
                        CircleAttached = True
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            SwappableCircles = list()
            if CircleAttached:
                for node in b.nodeList:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if node.isPointInBounds(mouse_x, mouse_y):
                        SwappableCircles.append(node)

                if len(SwappableCircles) == 2:
                    if validMove(*SwappableCircles) and target.color == Mycolor:
                        print(target.color)
                        color = SwappableCircles[0].color
                        SwappableCircles[0].color = SwappableCircles[1].color
                        SwappableCircles[1].color = color

            if target != None:
                target.pos = (original_x, original_y)
            MousePressed = False
            target = None
            CircleAttached = False

    if (MousePressed and target != None):
        target.pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    # Update screen
    screen.fill((0,0,0))  # Clear screen with white color
    # Draw the circle
    draw_text("Dupa",text_font, (255,255,255),50,50)
    screen

    for node in b.nodeList:
        node.draw(screen)

    pygame.display.flip()

pygame.quit()