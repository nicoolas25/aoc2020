import fileinput

first_line, second_line = [line.strip() for line in fileinput.input()]

# Part 1
# departure_time = int(first_line)
# line_numbers = [int(line_nr) for line_nr in second_line.split(',') if line_nr != 'x']
# last_stops = ((ln, (departure_time // ln) * ln) for ln in line_numbers)
# next_stops = ((ln, ls + ln if ls < departure_time else ls) for ln, ls in last_stops)
# next_line_nr, next_time = sorted(next_stops, key=lambda t: t[1])[0]
# print(next_line_nr * (next_time - departure_time))

# Part 2 - Chinese remainders https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
# 0, 1,   , 4,  6, 7
# 7,13,x,x,59,x,31,19
#
# n = 0 [7]
# n = 1 [13]
# n = 4 [59]
# n = 6 [31]
# n = 7 [19]

from collections import namedtuple

CRC = namedtuple('ChineseRemainderCongruence', ['remainder', 'modulo'])

def chinese_remainders(items):
    sorted_items = sorted(items, key=lambda x: x.modulo, reverse=True)
    item = sorted_items[0]
    n = item.modulo - item.remainder
    step = item.modulo
    seen = {item.modulo}
    while True:
        for item in sorted_items:
            if (n + item.remainder) % item.modulo != 0:
                n += step
                break
            elif item.modulo not in seen:
                seen.add(item.modulo)
                step *= item.modulo
        else:
            return n

print(chinese_remainders([
    CRC(remainder=diff, modulo=int(line_nr))
    for diff, line_nr in enumerate(second_line.split(','))
    if line_nr != 'x'
]))
