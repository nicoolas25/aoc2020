import fileinput

translation = str.maketrans("FBLR", "0101")
def seat_id(line):
    print(line)
    print(line.translate(translation))
    print(int(line.translate(translation), 2))
    return int(line.translate(translation), 2)

seat_ids = [
    seat_id(line.strip())
    for line in fileinput.input()
]

seat_ids = sorted(seat_ids)
for i, seat_id in enumerate(seat_ids):
    if seat_ids[i+1] != (seat_id + 1):
        print(seat_id + 1)
        break
