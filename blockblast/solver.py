from block import Block
from selection import Selection
from grid import Grid


def solve(grid, blocks):
    return backtrack(grid, blocks, [])


def backtrack(
    grid: Grid, selection: Selection, placements: list[tuple[Block, tuple[int, int]]]
) -> list[tuple[Block, tuple[int, int]]] | None:
    if not any(grid.can_place(b) for b in selection.blocks):
        return None

    prev_grid = grid.copy()

    for idx in range(len(selection.blocks)):
        block = selection.blocks[idx]

        possible_positions = [
            (y, x)
            for y in range(grid.size - block.height + 1)
            for x in range(grid.size - block.width + 1)
        ]
        possible_positions.sort(
            reverse=True, key=lambda p: get_num_cleared(grid, block, p)
        )

        for position in possible_positions:
            if grid.can_place(block, position):
                grid.place(block, position)

                placements.append((block, position))
                grid.clear_full()
                selection.blocks.pop(idx)

                if not len(selection.blocks):
                    return placements

                if result := backtrack(grid, selection, placements):
                    return result

                selection.blocks.insert(idx, block)
                for r in range(grid.size):
                    for c in range(grid.size):
                        grid.values[r][c] = prev_grid.values[r][c]
                placements.pop()

    return None


def get_num_cleared(grid: Grid, block: Block, position: tuple) -> int:
    grid_copy = grid.copy()

    if grid_copy.place(block, position):
        return grid_copy.clear_full()
    return -1


if __name__ == "__main__":
    grid = Grid(
        values=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )

    selection = Selection(
        [
            Block("1x1"),
            Block("2x2"),
            Block("3x3"),
        ]
    )

    print("\n", grid, "\n", sep="")

    if solution := solve(grid, selection):
        for block_idx, position in solution:
            print(position)
            print(block_idx)
        print()

        print(grid, "\n", sep="")
    else:
        print("No solution")
