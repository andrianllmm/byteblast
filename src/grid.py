import pygame
from typing import Optional

from config import GRID_SIZE, TILE_SIZE, COLOR_PALETTE
from block import Block


class Grid:
    def __init__(
        self, size: int = GRID_SIZE, values: Optional[list[list]] = None
    ) -> None:
        """Initialize the grid with a specified size."""
        self.values: list[list] = (
            [[0] * size for _ in range(size)] if not values else values
        )
        self.size: int = len(self.values)

    def can_place(
        self, block: Block, position: Optional[tuple[int, int]] = None
    ) -> bool:
        """Check if a block can be placed at a given position on the grid."""
        if not block:
            return False

        if position:
            return self.is_within_bounds(block, position) and not self.has_collision(
                block, position
            )

        for i in range(self.size - block.height + 1):
            for j in range(self.size - block.width + 1):
                if self.can_place(block, (i, j)):
                    return True
        return False

    def is_within_bounds(self, block: Block, position: tuple[int, int]) -> bool:
        """Check if a block is within the bounds of the grid."""
        y, x = position
        return (
            0 <= y < self.size
            and 0 <= x < self.size
            and y + block.height <= self.size
            and x + block.width <= self.size
        )

    def has_collision(self, block: Block, position: tuple[int, int]) -> bool:
        """Check if a block collides with existing blocks at a position."""
        for i in range(block.height):
            for j in range(block.width):
                y, x = position[0] + i, position[1] + j
                if block.shape[i][j] == 1 and self.values[y][x] == 1:
                    return True
        return False

    def place(self, block: Block, position: tuple[int, int]) -> bool:
        """Place a block on the grid at a given position."""
        if not self.can_place(block, position):
            return False
        for i in range(block.height):
            for j in range(block.width):
                if block.shape[i][j] == 1:
                    y, x = position[0] + i, position[1] + j
                    self.values[y][x] = 1
        return True

    def clear_full(self) -> int:
        """Clear full rows and columns."""
        count = 0
        for y in range(self.size):
            if all(self.values[y]):
                self.values[y] = [0] * self.size
                count += 1
        for x in range(self.size):
            if all(self.values[y][x] == 1 for y in range(self.size)):
                for y in range(self.size):
                    self.values[y][x] = 0
                count += 1
        return count

    def copy(self):
        """Make a copy of the current grid."""
        return Grid(values=[row[:] for row in self.values])

    def render(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        """Render the grid onto the screen."""
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(
                    x * TILE_SIZE + offset[0],
                    y * TILE_SIZE + offset[1],
                    TILE_SIZE,
                    TILE_SIZE,
                )
                if self.values[y][x] == 1:
                    pygame.draw.rect(screen, COLOR_PALETTE["tile"], rect)
                pygame.draw.rect(screen, COLOR_PALETTE["fore"], rect, 1)

    def __repr__(self):
        return "\n".join(
            " ".join(f"{'■' if c else '□'}" for c in r) for r in self.values
        )

    def __str__(self):
        return self.__repr__()
