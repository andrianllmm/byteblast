import pygame
import random

from config import SCREEN_RECT, TILE_SIZE, COLOR_PALETTE
from block import Block
from selection import Selection
from grid import Grid
from solver import solve


class BlockBlast:
    def __init__(
        self,
        screen: pygame.Surface = None,
        screen_rect: pygame.Rect = pygame.Rect(*SCREEN_RECT),
        grid: Grid = None,
        selection: Selection = None,
        score: int = 0,
        move_delay: int = 100,
        last_move_time: int = 0,
        auto_solve: bool = False,
    ) -> None:
        if screen is None:
            screen = pygame.display.set_mode(screen_rect.size)
        if grid is None:
            grid = Grid()
        if selection is None:
            selection = Selection()

        self.screen: pygame.Surface = screen
        self.screen_rect: pygame.Rect = screen_rect
        self.grid: Grid = grid
        self.selection: Selection = selection
        self.score: int = score
        self.move_delay: int = move_delay
        self.last_move_time: int = last_move_time
        self.auto_solve: bool = auto_solve
        self.running: bool = False

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_rect.size)
        pygame.display.set_caption("Block Blast")
        self.font = pygame.font.SysFont("Arial", 24)

    def loop(self) -> None:
        """Main game loop."""
        self.running = True
        while self.running:
            self.handle_events()
            self.handle_movement()

            if self.auto_solve:

                solution = solve(self.grid.copy(), self.selection.copy())

                if not solution:
                    self.game_over()
                    self.running = False
                    break

                for block, position in solution:
                    idx = -1
                    for i, b in enumerate(self.selection.blocks):
                        if block.shape == b.shape:
                            idx = i
                    self.selection.select(idx, initial_position=position)
                    if not self.grid.can_place(
                        self.selection.active, self.selection.active.position
                    ):
                        raise ValueError(
                            f"Block\n{block}\ncannot be placed at {position}"
                        )
                    self.place_block()

                    self.render()

                    pygame.time.delay(100)

            else:
                if not any(self.grid.can_place(b) for b in self.selection.blocks):
                    self.game_over()
                    self.running = False
                    break

            self.render()

        self.quit()

    def toggle_auto_solve(self) -> None:
        """Toggle the auto-solve mode."""
        self.auto_solve = not self.auto_solve

    def handle_events(self) -> None:
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def handle_keydown(self, event: pygame.event.Event) -> None:
        """Handle key press events."""
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.toggle_auto_solve()
        elif event.key == pygame.K_SPACE:
            self.place_block()
        elif event.key == pygame.K_TAB:
            self.selection.cycle()
        elif event.key in [pygame.K_a, pygame.K_s, pygame.K_d]:
            self.quick_select(event.key)

    def quick_select(self, key: int) -> None:
        """Select a block with ASD keys."""
        key_to_idx = {pygame.K_a: 0, pygame.K_s: 1, pygame.K_d: 2}
        idx = key_to_idx.get(key)
        if idx is not None and idx < self.selection.len():
            self.selection.select(idx)

    def handle_movement(self) -> None:
        """Move block with arrow keys."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_block(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.move_block(1, 0)
        elif keys[pygame.K_UP]:
            self.move_block(0, -1)
        elif keys[pygame.K_DOWN]:
            self.move_block(0, 1)
        self.last_move_time = current_time

    def move_block(self, dx: int, dy: int) -> None:
        """Move the active block by dx and dy."""
        self.selection.active.position = (
            self.selection.active.position[0] + dy,
            self.selection.active.position[1] + dx,
        )

    def place_block(self) -> None:
        """Place the active block on the grid and update score."""
        if self.grid.place(self.selection.active, self.selection.active.position):
            self.score += self.selection.active.tile_count
            self.score += self.grid.clear_full()
            self.selection.pop()
            if self.selection.len() <= 0:
                self.spawn_blocks()

    def spawn_blocks(self) -> None:
        """Spawns new blocks in selection."""
        blocks = [
            random.choice([b for b in Block.all_blocks() if self.grid.can_place(b)])
        ]
        self.complete_blocks(blocks)
        self.selection.spawn(blocks)

    def complete_blocks(self, blocks: list[Block]) -> bool:
        """Append blocks that are solvable."""
        if len(blocks) == 3:
            if solve(self.grid.copy(), Selection([b.copy() for b in blocks])):
                return True
            return False

        shuffled_blocks = Block.all_blocks()[:]
        random.shuffle(shuffled_blocks)

        for block in shuffled_blocks:
            blocks.append(block)
            if self.complete_blocks(blocks):
                return True
            blocks.pop()

        return False

    def render_score(self, offset: tuple[int, int] = (0, 0)) -> None:
        """Render the score."""
        score_text = self.font.render(f"{self.score}", True, COLOR_PALETTE["fore"])
        self.screen.blit(score_text, offset)

    def render(self) -> None:
        """Render the game screen."""
        self.screen.fill(COLOR_PALETTE["back"])
        offset = (2 * TILE_SIZE, 1 * TILE_SIZE)
        self.grid.render(self.screen, offset=offset)
        self.selection.active.render(
            self.screen,
            position=self.selection.active.position,
            offset=offset,
            fill_color=COLOR_PALETTE[
                (
                    "tile"
                    if self.grid.can_place(
                        self.selection.active, self.selection.active.position
                    )
                    else "tile-error"
                )
            ],
        )
        self.selection.render(self.screen, offset=(0, offset[1]))
        self.render_score((10, 10))
        pygame.display.flip()

    def game_over(self) -> None:
        """Display game over."""
        print("Game over!")
        pygame.time.delay(2500)

    def quit(self) -> None:
        pygame.quit()


def start_game() -> None:
    game = BlockBlast()
    game.loop()


if __name__ == "__main__":
    start_game()
