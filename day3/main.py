import fileinput

tower = [line.strip() for line in fileinput.input()]
width = len(tower[0])

def trees(diff_x, diff_y):
    trees = 0
    x, y = 0, 0
    while True:
        if len(tower) <= y:
            break

        if tower[y][x % width] == "#":
            trees += 1

        x, y = (x + diff_x), (y + diff_y)
    return trees

print(trees(1, 1) * trees(3, 1) * trees(5, 1) * trees(7, 1) * trees(1, 2))
