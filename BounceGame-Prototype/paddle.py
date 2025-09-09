# paddly.py
from config import *
import pygame

# -------------------------------------------------------------
#   Object class for paddles
# -------------------------------------------------------------
class Paddle:
    def __init__(self, left, top, width, height, color, vertical=False):
        # "Flip" paddle params if requested, for vertical movement
        if vertical:
            self.hitbox = pygame.Rect(
                left,
                top,
                height,
                width,
            )
        else:
            self.hitbox = pygame.Rect(
                left,
                top,
                width,
                height,
            )
        self.color = color
        self.vertical = vertical

    # ------------------------------------------------------------------
    # Movement – flip input to y if vertical mode
    # ------------------------------------------------------------------
    def move(self, direction):
        # direction: -1 left/up, +1 right/down, 0 stopped.
        if self.vertical:
            self.hitbox.y += direction * PADDLE_SPEED
            self.hitbox.y = max(WIN_MARGIN, min(self.hitbox.y, (PLAYFIELD_HEIGHT - WIN_MARGIN) - self.hitbox.height))
        else:
            self.hitbox.x += direction * PADDLE_SPEED
            self.hitbox.x = max(WIN_MARGIN, min(self.hitbox.x, PLAYFIELD_WIDTH - self.hitbox.width))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.hitbox)