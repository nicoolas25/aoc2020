import fileinput

grid = [list(line.strip()) for line in fileinput.input()]
height, width = len(grid), len(grid[0])

directions = [
    (di, dj)
    for dj in range(-1, 2)
    for di in range(-1, 2)
    if di != 0 or dj != 0
]

def occupied_visible_count(grid, i, j, closest=True):
    count = 0
    for di, dj in directions:
        ii, jj = i + di, j + dj
        while ii >= 0 and ii < height and jj >= 0 and jj < width:
            seat = grid[ii][jj]
            if seat == '#':
                count += 1
                break
            if seat == 'L' or closest:
                break
            ii, jj = ii + di, jj + dj
    return count

def next_grid(grid, closest=False, raise_limit=5):
    next_grid = []
    for i in range(height):
        row = []
        for j in range(width):
            cell = grid[i][j]
            if cell == 'L' and occupied_visible_count(grid, i, j, closest) == 0:
                row.append('#')
            elif cell == '#' and occupied_visible_count(grid, i, j, closest) >= raise_limit:
                row.append('L')
            else:
                row.append(cell)
        next_grid.append(row)
    return next_grid

while True:
    n_grid = next_grid(grid)
    if n_grid == grid:
        occupied_seats = sum(sum(1 for seat in row if seat == '#') for row in grid)
        print(occupied_seats)
        break
    else:
        grid = n_grid
