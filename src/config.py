GRID_SIZE = 8
TILE_SIZE = 50

SCREEN_WIDTH = round((GRID_SIZE * 1.5) * TILE_SIZE)
SCREEN_HEIGHT = round((GRID_SIZE * 1.7) * TILE_SIZE)
SCREEN_RECT = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

COLOR_PALETTE = {
    "back": (0, 0, 0),
    "fore": (72, 101, 64),
    "tile": (194, 214, 166),
    "tile-muted": (124, 132, 110),
    "tile-error": (129, 11, 71),
}

FONT_NAME = "Arial"
FONT_SIZE = 24
