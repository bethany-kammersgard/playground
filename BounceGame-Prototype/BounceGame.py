#!/usr/bin/env python3
# -------------------------------------------------------------
#   Silly little test game
#   Bouncing Ball + 4 Platforms
#   Play by just running "python .\BounceGame.py" on terminal
# -------------------------------------------------------------
import sys
from playfield import Playfield
# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
def main():
    Playfield().run()
    sys.exit(0)

if __name__ == "__main__":
    main()
