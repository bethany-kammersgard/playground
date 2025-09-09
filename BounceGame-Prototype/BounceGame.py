#!/usr/bin/env python3
# -------------------------------------------------------------
#   Silly little test game
#   Bouncing Ball + 4 Platforms
#   Score = number of seconds the ball stays in the air
#   Ball speeds up gradually
#   Play by just running "python .\BounceGame" on terminal
# -------------------------------------------------------------

import pygame
import sys

# -------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600           # Window size
FPS = 60                           # Frames per second

PADDLE_HEIGHT = 20
PADDLE_COLOR = (200, 200, 50)
BALL_COLOR = (250, 50, 50)
BG_COLOR = (30, 30, 30)

BALL_RADIUS = 15
GRAVITY = 0.95          # Pixels per frame
INITIAL_BALL_SPEED = 10 # Initial vertical speed
SPEED_UP_RATE = 0.0005  # How much faster each frame

PLATFORM_SPEED = 7      # Horizontal speed of the platform
MAX_PLATFORM_SPEED = 12

# -------------------------------------------------------------
# PLATFORM CLASS
# -------------------------------------------------------------
class QuadPaddle:
    def __init__(self):
        # 4 paddles.
        self.width = WIN_WIDTH // 4
        # X axis paddles (top and bottom)
        self.top = pygame.Rect(
            (WIN_WIDTH - self.width) // 2,
            int(WIN_HEIGHT * 0.9),
            self.width,
            PADDLE_HEIGHT,
        )
        self.bot = pygame.Rect(
            (WIN_WIDTH - self.width) // 2,
            int(WIN_HEIGHT * 0.1),
            self.width,
            PADDLE_HEIGHT,
        )
        self.pos_x = 0
        self.vel_x = 0

    def update(self, keys):
        """Move left/right based on pressed keys."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLATFORM_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLATFORM_SPEED
        else:
            self.vel_x = 0

        # Update position and clamp to screen edges
        self.pos_x += self.vel_x
        if self.top.left < 0:
            self.pos_x = 0
        if self.top.right > WIN_WIDTH:
            self.pos_x = WIN_WIDTH - self.width
        self.top.x = self.pos_x
        self.bot.x = self.pos_x

    def draw(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, self.top)
        pygame.draw.rect(screen, PADDLE_COLOR, self.bot)

# -------------------------------------------------------------
# BALL CLASS
# -------------------------------------------------------------
class Ball:
    def __init__(self, paddles):
        self.paddles = paddles
        self.reset()

    def reset(self):
        self.x = WIN_WIDTH // 2
        self.y = WIN_HEIGHT // 2  # start in center
        self.vx = 0
        self.vy = INITIAL_BALL_SPEED
        self.speed_multiplier = 1.0

    def update(self, dt, screen):
        """Physics update."""
        # Gravity
        self.vy += GRAVITY * self.speed_multiplier

        # Horizontal motion (none, but could be added)
        self.x += self.vx * dt

        # Update position
        self.y += self.vy * dt

        # Check collision with platform
        if self.vy > 0 or self.vy < 0:
            hitbox = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
            if self.paddles.top.colliderect(hitbox) or self.paddles.bot.colliderect(hitbox):
                # Bounce: invert velocity and add a small bounce boost
                self.vy = -self.vy * 1.1
                self.speed_multiplier += SPEED_UP_RATE  # speed up a bit
                # Horizontal tweak based on platform speed and position on platform
                english_factor = -2.5
                self.vx += (self.paddles.vel_x * english_factor) + (self.x - self.paddles.pos_x)

        # Floor collision (lose condition)
        if self.y - BALL_RADIUS > WIN_HEIGHT or self.y - BALL_RADIUS < 0:
            return False  # ball fell

        # Left/right wall bounce
        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > WIN_WIDTH:
            self.vx = -self.vx

        return True  # ball still alive

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

# -------------------------------------------------------------
# INITIALISE PYGAME
# -------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("BounceGame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# -------------------------------------------------------------
# MAIN GAME LOOP
# -------------------------------------------------------------
def main():
    paddles = QuadPaddle()
    ball = Ball(paddles)
    start_ticks = pygame.time.get_ticks()  # ms
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0  # convert to seconds

        # ---------- EVENT PROCESSING ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # ---------- UPDATE ----------
        paddles.update(keys)
        alive = ball.update(dt, screen)

        if not alive:
            # Game over: show final score, wait a bit, then quit
            elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0
            print(f"Game over! Score: {int(elapsed)} seconds")
            pygame.time.wait(2000)
            running = False
            continue

        # ---------- DRAW ----------
        screen.fill(BG_COLOR)
        paddles.draw(screen)
        ball.draw(screen)

        # Show score
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0
        score_surf = font.render(f"Score: {int(elapsed)} s", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    main()
