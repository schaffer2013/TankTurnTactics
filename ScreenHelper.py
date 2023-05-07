import pygame

# Define some colors
BLACK = (0, 0, 0)
LIGHT_GRAY = (140, 140, 140)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (128, 0, 128)
LIGHT_PURPLE = (203, 195, 227)

ACTIVE = GREEN
INACTIVE = LIGHT_BLUE


def displayText(screen, font, text, textCenterX, textCenterY, color=(0, 0, 0)):
    text = font.render(str(text), True, color)
    text_rect = text.get_rect(center=(textCenterX, textCenterY))
    screen.blit(text, text_rect)


def drawRedCircle(screen, xy, radius, draw_top_left=False, draw_top_right=False, draw_bottom_left=False, draw_bottom_right=False):
    pygame.draw.circle(screen,
                       RED,
                       (xy[0], xy[1]),
                       radius,
                       draw_top_left=draw_top_left,
                       draw_top_right=draw_top_right,
                       draw_bottom_left=draw_bottom_left,
                       draw_bottom_right=draw_bottom_right)


def drawCell(c, r, color, screen, margin, height, width):
    tempX = (margin + width) * c + margin
    tempY = (margin + height) * r + margin
    pygame.draw.rect(screen,
                     color,
                     [tempX, tempY, width, height])
