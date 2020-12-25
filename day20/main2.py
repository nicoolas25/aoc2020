from fileinput import input

pattern = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]

active_cells = [
    (i, j)
    for i, line in enumerate(pattern)
    for j, cell in enumerate(line)
    if cell == '#'
]

class Pattern:
    def __init__(self, active_cells):
        self.active_cells = set(active_cells)

    def variations(self):
        t = self
        for _ in range(4):
            yield t
            yield t._flip()
            t = t._rotate_right()

    def _rotate_right(self):
        rotated_cells = ((j, -i + 9) for i, j in self.active_cells)
        return Pattern(rotated_cells)

    def _flip(self):
        flipped_cells = ((i, 9 - j) for i, j in self.active_cells)
        return Pattern(flipped_cells)

lines = [line.strip() for line in input()]

SIZE = len(lines)

grid = {
    (i, j)
    for i, line in enumerate(lines)
    for j, cell in enumerate(line)
    if cell == '#'
}

def match(pattern, pi, pj):
    candidates = list(map(lambda p: (p[0] + pi, p[1] + pj), pattern.active_cells))
    return candidates if all(candidate in grid for candidate in candidates) else []

matches = set()
patterns = list(Pattern(active_cells).variations())
for i in range(SIZE):
    for j in range(SIZE):
        for pattern in patterns:
            matched_positions = match(pattern, i, j)
            matches = matches.union(matched_positions)

print(len(grid) - len(matches))
