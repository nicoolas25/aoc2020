import fileinput
from collections import defaultdict
from functools import reduce

# Reading the file

lines = [line.strip() for line in fileinput.input()]

constraints = []
while (constraint_line := lines.pop(0)) != '':
    name, ranges_str = constraint_line.split(': ')
    ranges = [
        tuple(map(int, r.split('-')))
        for r in ranges_str.split(' or ')
    ]
    constraints.append((name, ranges))

lines.pop(0) # your ticket legend

your_ticket = [int(d) for d in lines.pop(0).split(',')]

lines.pop(0) # blank line
lines.pop(0) # nearby tickets legend

nearby_tickets = []
while lines:
    nearby_tickets.append([
        int(d)
        for d in lines.pop(0).split(',')
    ])

# Part 2

def satisfy_any_constraint(value):
    for _name, ranges in constraints:
        for lower, upper in ranges:
            if lower <= value <= upper:
                return True
    return False

valid_tickets = [
    ticket
    for ticket in nearby_tickets
    if all(satisfy_any_constraint(value) for value in ticket)
]

fields = defaultdict(lambda: [name for name, _ in constraints])
for ticket in valid_tickets:
    for index, value in enumerate(ticket):
        for name, ranges in constraints:
            (l1, u1), (l2, u2) = ranges
            if not (l1 <= value <= u1 or l2 <= value <= u2):
                fields[index].remove(name)

for index, possible_fields in sorted(fields.items(), key=lambda f: len(f[1])):
    if len(possible_fields) == 1:
        for candidate_index, candidate_fields in fields.items():
            if candidate_index != index:
                try:
                    candidate_fields.remove(possible_fields[0])
                except ValueError:
                    pass

print(
    reduce(
        (lambda x, y: x * y),
        [
            your_ticket[index]
            for index, names in fields.items()
            if names[0][:9] == 'departure'
        ],
    )
)
