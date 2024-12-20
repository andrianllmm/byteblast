import pygame
from random import shuffle
from typing import Optional

from config import SCREEN_WIDTH, GRID_SIZE, TILE_SIZE, COLOR_PALETTE
from block import Block


class Selection:
    def __init__(self, blocks: Optional[list[Block]] = None) -> None:
        """Initialize the selection with random blocks."""
        if blocks:
            self.blocks: list[Block] = blocks
            self.idx: int = 0
            self.active: Block = self.blocks[self.idx]
        else:
            self.spawn()

    def spawn(self, blocks: Optional[list[Block]] = None) -> None:
        """Spawn a set of unique random blocks."""
        N = 3
        if blocks and len(blocks) == N:
            self.blocks = blocks
        else:
            all_blocks = Block.all_blocks()
            shuffle(all_blocks)
            self.blocks = all_blocks[:N]
        self.idx = 0
        self.active = self.blocks[self.idx]

    def select(
        self, idx: int, initial_position: Optional[tuple[int, int]] = None
    ) -> None:
        """Set the active block with index."""
        if not initial_position:
            initial_position = self.active.position

        if idx < self.len():
            self.idx = idx
            self.active = self.blocks[self.idx]

        self.active.position = initial_position

    def cycle(self) -> None:
        """Cycle to the next block in the selection."""
        self.idx = (self.idx + 1) % len(self.blocks)
        self.select(self.idx)

    def pop(self, idx: Optional[int] = None) -> None:
        """Remove a block from the selection with index."""
        idx = idx or self.idx
        self.blocks.pop(idx)

        if self.len() > 0:
            self.select(0)

    def len(self) -> int:
        """Evaluate the number of blocks in the selection."""
        return len(self.blocks)

    def copy(self):
        """Make a copy of the current selection."""
        return Selection(blocks=[block.copy() for block in self.blocks])

    def render(
        self,
        screen: pygame.Surface,
        offset: tuple[int, int] = (0, 0),
        tile_size: int = TILE_SIZE // 2,
    ) -> None:
        """Render all blocks in the selection on the screen."""
        spacing = 3 * tile_size
        width = (
            sum(block.width for block in self.blocks if isinstance(block, Block))
            * tile_size
            + (self.len() - 1) * spacing
        )
        offset_x = offset[0] + (SCREEN_WIDTH - width) // 2
        offset_y = (GRID_SIZE) * TILE_SIZE + tile_size + offset[1]

        for i, block in enumerate(b for b in self.blocks if b):
            fill_color = COLOR_PALETTE["tile" if self.idx == i else "tile-muted"]
            block.render(
                screen,
                fill_color=fill_color,
                position=(0, 0),
                offset=(offset_x, offset_y),
                tile_size=tile_size,
            )
            offset_x += block.width * tile_size + spacing

    def __repr__(self):
        return "\n\n".join(f"{b}" for b in self.blocks)

    def __str__(self):
        return self.__repr__()
