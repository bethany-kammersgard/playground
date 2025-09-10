# ball.py
import pygame
from config import *

# -------------------------------------------------------------
#   Object class for ball
# -------------------------------------------------------------
class Ball:
    def __init__(self, paddles):
        self.paddles = paddles      # List of Paddle objects
        self.reset()

    def reset(self):
        self.x = (WIN_MARGIN + PLAYFIELD_WIDTH) // 2
        self.y = PLAYFIELD_HEIGHT // 2    # Ball 0 position is center of screen
        self.vx = 0
        self.vy = INITIAL_VEL
        self.speed_multiplier = 1.0

    # ------------------------------------------------------------------
    # Physics + collision
    # ------------------------------------------------------------------
    def update(self, dt):
        # Gravity
        self.vy += GRAVITY * self.speed_multiplier

        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Ball hitbox for collision checks
        hitbox = pygame.Rect(
            self.x - BALL_RADIUS, self.y - BALL_RADIUS,
            BALL_RADIUS*2, BALL_RADIUS*2
        )

        # ----------------------------------------------------------------
        # Collide with *any* paddle
        # ----------------------------------------------------------------
        for paddle in self.paddles:
            if paddle.hitbox.colliderect(hitbox):
                # Bounce off paddle: invert velocity plus tweak based on position ball hits on paddle
                if paddle.vertical:
                    self.vx = -self.vx
                    self.vy += self.y - paddle.hitbox.y
                else:
                    self.vy = -self.vy
                    self.vx += self.x - paddle.hitbox.x
                self.speed_multiplier += SPEED_UP_RATE  # speed up a bit
                break  # Limit only one collision per frame

        # ----------------------------------------------------------------
        # Edge collisions (falling out of bounds)
        # ----------------------------------------------------------------
        if self.y - BALL_RADIUS > PLAYFIELD_HEIGHT or self.y + BALL_RADIUS < 0:
            return False  # ball lost

        return True

    def draw(self, surf):
        pygame.draw.circle(surf, PNK_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)
