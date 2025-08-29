#!/usr/bin/env python3
# -------------------------------------------------------------
#   Silly little test game
#   Bouncing Ball + Platform
#   Score = number of seconds the ball stays in the air
#   Ball speeds up gradually
#   Play by just running "python .\BounceGame" on terminal
# -------------------------------------------------------------

import pygame
import sys

# -------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------
WIDTH, HEIGHT = 800, 600           # Window size
FPS = 60                           # Frames per second

PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (200, 200, 50)
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
class Platform:
    def __init__(self):
        # Start in the middle, 80% of screen height
        self.width = WIDTH // 4
        self.rect = pygame.Rect(
            (WIDTH - self.width) // 2,
            int(HEIGHT * 0.8),
            self.width,
            PLATFORM_HEIGHT,
        )
        self.speed = 0

    def update(self, keys):
        """Move left/right based on pressed keys."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed = -PLATFORM_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed = PLATFORM_SPEED
        else:
            self.speed = 0

        # Update position and clamp to screen edges
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, PLATFORM_COLOR, self.rect)

# -------------------------------------------------------------
# BALL CLASS
# -------------------------------------------------------------
class Ball:
    def __init__(self, platform):
        self.platform = platform
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = 50  # start near top
        self.vx = 0
        self.vy = INITIAL_BALL_SPEED
        self.speed_multiplier = 1.0

    def update(self, dt):
        """Physics update."""
        # Gravity
        self.vy += GRAVITY * self.speed_multiplier

        # Horizontal motion (none, but could be added)
        self.x += self.vx * dt

        # Update position
        self.y += self.vy * dt

        # Check collision with platform
        if self.vy > 0:  # only when falling
            hitbox = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
            if self.platform.rect.colliderect(hitbox):
                # Bounce: invert velocity and add a small bounce boost
                self.vy = -self.vy * 1.1
                self.speed_multiplier += SPEED_UP_RATE  # speed up a bit
                # Horizontal tweak based on platform speed and position on platform
                english_factor = -2.5
                self.vx += (self.platform.speed * english_factor) + (self.x - self.platform.rect.centerx)

        # Floor collision (lose condition)
        if self.y - BALL_RADIUS > HEIGHT:
            return False  # ball fell

        # Ceiling bounce
        if self.y - BALL_RADIUS < 0:
            self.vy = -self.vy

        # Left/right wall bounce
        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > WIDTH:
            self.vx = -self.vx

        return True  # ball still alive

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

# -------------------------------------------------------------
# INITIALISE PYGAME
# -------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BounceGame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# -------------------------------------------------------------
# MAIN GAME LOOP
# -------------------------------------------------------------
def main():
    platform = Platform()
    ball = Ball(platform)
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
        platform.update(keys)
        alive = ball.update(dt)

        if not alive:
            # Game over: show final score, wait a bit, then quit
            elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0
            print(f"Game over! Score: {int(elapsed)} seconds")
            pygame.time.wait(2000)
            running = False
            continue

        # ---------- DRAW ----------
        screen.fill(BG_COLOR)
        platform.draw(screen)
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
