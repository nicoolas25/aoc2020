import fileinput

active_cells = {
    (x, y, 0, 0)
    for x, line in enumerate(fileinput.input())
    for y, cell in enumerate(line.strip())
    if cell == '#'
}

def neighbors(x, y, z, w):
    for xn in range(-1, 2):
        for yn in range(-1, 2):
            for zn in range(-1, 2):
                for wn in range(-1, 2):
                    if xn == 0 and yn == 0 and zn == 0 and wn == 0:
                        continue
                    else:
                        yield (x + xn, y + yn, z + zn, w + wn)

def active_neighbors_count(coordinate, active_cells):
    return sum(1 for cell in neighbors(*coordinate) if cell in active_cells)

def tick(active_cells):
    dying_cells = {
        cell
        for cell in active_cells
        if not (2 <= active_neighbors_count(cell, active_cells) <= 3)
    }
    born_cells = {
        ncell
        for cell in active_cells
        for ncell in neighbors(*cell)
        if ncell not in active_cells
        and active_neighbors_count(ncell, active_cells) == 3
    }
    return (active_cells - dying_cells) | born_cells


print(len(tick(tick(tick(tick(tick(tick(active_cells))))))))
