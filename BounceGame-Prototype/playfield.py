# playfield.py
import pygame
from config import *
from paddle import Paddle
from ball   import Ball
#from target import Target      # TODO

# -------------------------------------------------------------
#   Composite class for that owns and orchestrates all game objects
# -------------------------------------------------------------
class Playfield:
    def __init__(self):
        # Create the four paddles (our passive player controlled objects)
        self.x_paddles = [
            Paddle((WIN_MARGIN + PLAYFIELD_WIDTH-PADDLE_LENGTH)//2, PLAYFIELD_HEIGHT*0.9, PADDLE_LENGTH, PADDLE_GIRTH, RED_COLOR),            # top
            Paddle((WIN_MARGIN + PLAYFIELD_WIDTH-PADDLE_LENGTH)//2, PLAYFIELD_HEIGHT*0.1, PADDLE_LENGTH, PADDLE_GIRTH, GRN_COLOR),            # bottom
        ]
        self.y_paddles = [
            Paddle(WIN_MARGIN, (PLAYFIELD_HEIGHT-PADDLE_LENGTH)//2, PADDLE_LENGTH, PADDLE_GIRTH, YEL_COLOR, vertical=True),      # left
            Paddle(PLAYFIELD_WIDTH - PADDLE_GIRTH, (PLAYFIELD_HEIGHT-PADDLE_LENGTH)//2, PADDLE_LENGTH, PADDLE_GIRTH, BLU_COLOR, vertical=True)  # right
        ]

        # Create the ball (our active and reactive non player controlled object)
        self.ball = Ball(self.x_paddles + self.y_paddles)

        # optional: targets or power-ups
        #self.targets = [
        #    Target(pygame.Rect(300, 250, 40, 40))
        #]

        self.score = 0

        # Setup pygame stuff
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    # --------------------------------------------------------------
    # Input
    # --------------------------------------------------------------
    def handle_input(self, keys):
        # Catch key input and match to desired direction
        x_dir = 0
        y_dir = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x_dir = -1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y_dir = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x_dir = 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y_dir = 1
        # Move paddles, x paddles in "sync" then y paddles in "sync"
        for p in self.x_paddles:
            p.move(x_dir)
        for p in self.y_paddles:
            p.move(y_dir)

    # --------------------------------------------------------------
    # Update loop
    # --------------------------------------------------------------
    def update(self, dt):
        if not self.ball.update(dt):
            return False  # ball lost

        # Check targets TODO
        #ball_rect = self.ball.get_rect()
        #for t in self.targets:
        #    if t.check_collision(ball_rect):
        #        self.score += 10   # whatever

        # For now, increase score based on time in play
        self.score += dt

        return True

    # --------------------------------------------------------------
    # Draw loop
    # --------------------------------------------------------------
    def draw(self, screen):
        screen.fill(BG_COLOR)
        for p in self.x_paddles + self.y_paddles:
            p.draw(screen)
        #for t in self.targets: TODO
        #    t.draw(screen)
        self.ball.draw(screen)

        # Score
        text = self.font.render(f"Score: {round(self.score)}", True, (255,255,255))
        screen.blit(text, (10, 10))

    # --------------------------------------------------------------
    # Main loop wrapper
    # --------------------------------------------------------------
    def run(self):
        # Init screen and clock
        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("BounceGame")
        # Run loop
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.handle_input(keys)

            if not self.update(dt):
                print(f"Game over! Final score: {self.score}")
                pygame.time.wait(2000)
                running = False
                continue

            self.draw(screen)
            pygame.display.flip()
        # Game end - quit out
        pygame.quit()