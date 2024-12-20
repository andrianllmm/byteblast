import pygame
from random import choice
from typing import List, Tuple, Optional

from config import GRID_SIZE, TILE_SIZE, COLOR_PALETTE


BLOCKS = {
    "3x3": [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ],
    "2x2": [
        [1, 1],
        [1, 1],
    ],
    "1x1": [[1]],
    "1x2": [[1, 1]],
    "1x3": [[1, 1, 1]],
    "1x4": [[1, 1, 1, 1]],
    "1x5": [[1, 1, 1, 1, 1]],
    "2x3": [
        [1, 1, 1],
        [1, 1, 1],
    ],
    "diagonal-2": [
        [0, 1],
        [1, 0],
    ],
    "diagonal-3": [
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
    ],
    "corner-2": [
        [1, 0],
        [1, 1],
    ],
    "corner-3": [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
    ],
    "T": [
        [1, 1, 1],
        [0, 1, 0],
    ],
    "L": [
        [1, 0],
        [1, 0],
        [1, 1],
    ],
    "L-flipped": [
        [0, 1],
        [0, 1],
        [1, 1],
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 1],
    ],
    "Z-flipped": [
        [0, 1, 1],
        [1, 1, 0],
    ],
}


class Block:
    def __init__(self, shape: List[list] | str, rotation: int = 0) -> None:
        """Initialize a block with a given shape and rotation."""
        if isinstance(shape, list):
            self.shape: List[list] = shape
        elif isinstance(shape, str):
            if shape in BLOCKS:
                self.shape = BLOCKS[shape]
            else:
                raise ValueError(
                    f"Block name '{shape}' not found in predefined blocks."
                )
        else:
            raise TypeError(
                "Block data must be either a list (custom shape) or a string (block name)."
            )

        self.rotate(rotation)

        self._position: Tuple[int, int] = (0, 0)
        self.width: int = len(self.shape[0])
        self.height: int = len(self.shape)
        self.tile_count: int = sum(row.count(1) for row in self.shape)

    @property
    def position(self) -> Tuple[int, int]:
        """Get the current position of the block."""
        return self._position

    @position.setter
    def position(self, value: Tuple[int, int]) -> None:
        """Set the position of the block and adjust if out of bounds."""
        self._position = value
        self.adjust_position()

    def adjust_position(self) -> None:
        """Adjust the block's position to ensure it stays within grid bounds."""
        y, x = self._position
        if y + self.height > GRID_SIZE:
            y -= (y + self.height) - GRID_SIZE
        if x + self.width > GRID_SIZE:
            x -= (x + self.width) - GRID_SIZE
        self._position = (max(y, 0), max(x, 0))

    @classmethod
    def all_blocks(cls):
        """Generate all possible blocks."""
        if not hasattr(cls, "_all_blocks_cache"):
            cls._all_blocks_cache = [
                Block(b, rotation=r) for b in BLOCKS.keys() for r in [0, 90, 180, 270]
            ]
        return cls._all_blocks_cache

    @classmethod
    def random(cls, exclude: list = []) -> "Block":
        """Generate a random block with a random rotation."""
        return choice([b for b in cls.all_blocks() if b not in exclude])

    def rotate(self, deg: int = 0) -> None:
        """Rotate the block by the given degree."""
        m, n = len(self.shape), len(self.shape[0])
        if deg == 90:
            self.shape = [
                [self.shape[m - j - 1][i] for j in range(m)] for i in range(n)
            ]
        elif deg == 180:
            self.shape = [row[::-1] for row in self.shape][::-1]
        elif deg == 270:
            self.shape = [[self.shape[j][i] for j in range(m)] for i in range(n)]
        self.width = len(self.shape[0])
        self.height = len(self.shape)

    def copy(self):
        """Make a copy of the current block."""
        return Block(shape=[row[:] for row in self.shape])

    def render(
        self,
        screen: pygame.Surface,
        fill_color: Tuple[int, int, int] = COLOR_PALETTE["tile"],
        position: Optional[Tuple[int, int]] = None,
        offset: Tuple[int, int] = (0, 0),
        tile_size: int = TILE_SIZE,
    ) -> None:
        """Render the block on the screen at the specified position."""
        if not position:
            position = self.position
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] == 1:
                    x = (position[1] + col) * tile_size + offset[0]
                    y = (position[0] + row) * tile_size + offset[1]
                    rect = pygame.Rect(x, y, tile_size, tile_size)
                    pygame.draw.rect(screen, fill_color, rect)
                    pygame.draw.rect(screen, COLOR_PALETTE["fore"], rect, 1)

    def __repr__(self):
        return "\n".join(
            " ".join(f"{'■' if c else ' '}" for c in r) for r in self.shape
        )

    def __str__(self):
        return self.__repr__()
