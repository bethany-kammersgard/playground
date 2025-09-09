# config.py
# -------------------------------------------------------------
#   Config class with global values
# -------------------------------------------------------------
# Screen
WIN_WIDTH         = 700
WIN_HEIGHT        = 700
WIN_MARGIN        = 100
PLAYFIELD_WIDTH   = 600
PLAYFIELD_HEIGHT  = 600
FPS         = 60

# Colors
BG_COLOR = (30, 30, 30)
RED_COLOR = (250, 50, 50)
GRN_COLOR = (50, 250, 50)
BLU_COLOR = (50, 50, 250)
YEL_COLOR = (250, 250, 50)
PNK_COLOR = (250, 50, 200)

# Paddle sizes
PADDLE_LENGTH  = PLAYFIELD_WIDTH // 4
PADDLE_GIRTH   = 20

# Ball
BALL_RADIUS   = 15
GRAVITY       = 0.95
INITIAL_VEL   = 10
SPEED_UP_RATE = 0.0005

# Movement
PADDLE_SPEED  = 7
MAX_SPEED     = 12

# Font (init in Playfield)
FONT_NAME = None
FONT_SIZE = 36
