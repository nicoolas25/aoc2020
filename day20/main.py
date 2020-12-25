from fileinput import input
from collections import namedtuple
from functools import reduce
from math import sqrt

TILE_SIZE = 10
LAST_TILE_INDEX = TILE_SIZE - 1

class Tile:
    def __init__(self, number, active_cells):
        self.number = int(number)
        self.active_cells = set(active_cells)

    def left_matches_right_of(self, other_tile):
        for x in range(TILE_SIZE):
            if ((x, 0) in self.active_cells) != ((x, LAST_TILE_INDEX) in other_tile.active_cells):
                return False
        return True

    def top_matches_bottom_of(self, other_tile):
        for x in range(TILE_SIZE):
            if ((0, x) in self.active_cells) != ((LAST_TILE_INDEX, x) in other_tile.active_cells):
                return False
        return True

    def variations(self):
        t = self
        for _ in range(4):
            yield t
            yield t.flip()
            t = t.rotate_right()

    def rotate_right(self):
        rotated_cells = ((j, -i + 9) for i, j in self.active_cells)
        return Tile(self.number, rotated_cells)

    def flip(self):
        flipped_cells = ((i, 9 - j) for i, j in self.active_cells)
        return Tile(self.number, flipped_cells)

    def __str__(self):
        return '\n'.join(
            ' '.join(
                '#' if (i, j) in self.active_cells else '.'
                for j in range(TILE_SIZE)
            )
            for i in range(TILE_SIZE)
        )

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        return self.number == other.number

# Parsing

sections = [[]]
for line in map(str.strip, input()):
    if line:
        sections[-1].append(line)
    else:
        sections.append([])

all_tiles = []
for section in sections:
    if not section:
        continue
    first_line, *rest = section
    number = first_line.split(' ')[1][0:-1]
    active_cells = [
        (i, j)
        for i, line in enumerate(rest)
        for j, cell in enumerate(line)
        if cell == '#'
    ]
    all_tiles.append(Tile(number, active_cells))

PUZZLE_SIZE = int(sqrt(len(all_tiles)))

class PuzzleState:
    def __init__(self, positioned_tiles, remaining_tiles):
        self.positioned_tiles = positioned_tiles
        self.remaining_tiles= remaining_tiles

    def next_valid_tiles(self):
        for tile in self.remaining_tiles:
            for tile_variation in tile.variations():
                if self._valid(tile_variation):
                    yield tile_variation

    def position_tile(self, tile):
        return PuzzleState(
            positioned_tiles=[*self.positioned_tiles, tile],
            remaining_tiles=[t for t in self.remaining_tiles if t != tile],
        )

    def is_complete(self):
        return len(self.remaining_tiles) == 0

    def _valid(self, tile):
        next_tile_index = len(self.positioned_tiles)
        if next_tile_index >= PUZZLE_SIZE:
            top_index = next_tile_index - PUZZLE_SIZE
            top_tile = self.positioned_tiles[top_index]
            if not tile.top_matches_bottom_of(top_tile):
                return False
        if next_tile_index % PUZZLE_SIZE > 0:
            left_index = next_tile_index - 1
            left_tile = self.positioned_tiles[left_index]
            if not tile.left_matches_right_of(left_tile):
                return False
        return True

def solve(puzzle_state):
    if puzzle_state.is_complete():
        return puzzle_state
    else:
        for next_tile in puzzle_state.next_valid_tiles():
            next_puzzle_state = puzzle_state.position_tile(next_tile)
            solution_state = solve(next_puzzle_state)
            if solution_state:
                return solution_state
        return None

final_puzzle_state = solve(PuzzleState(positioned_tiles=[], remaining_tiles=all_tiles))

# Part 1
# if final_puzzle_state:
#     print(
#         final_puzzle_state.positioned_tiles[0].number *
#         final_puzzle_state.positioned_tiles[PUZZLE_SIZE - 1].number *
#         final_puzzle_state.positioned_tiles[-PUZZLE_SIZE].number *
#         final_puzzle_state.positioned_tiles[-1].number
#     )

# Part 2 - print the solution without the borders in order to find the sea monsters
# ----------------------
# |                  # |
# |#    ##    ##    ###|
# | #  #  #  #  #  #   |
# ----------------------

for ti in range(PUZZLE_SIZE):
    for i in range(1, TILE_SIZE - 1):
        line = []
        for tj in range(PUZZLE_SIZE):
            tile_index = ti * PUZZLE_SIZE + tj
            tile = final_puzzle_state.positioned_tiles[tile_index]
            for j in range(1, TILE_SIZE - 1):
                line.append('#' if (i, j) in tile.active_cells else '.')
        print(''.join(line))
