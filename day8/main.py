import fileinput

program = []
for line in fileinput.input():
    operation, argument = line.strip().split(' ', maxsplit=1)
    program.append((operation, int(argument)))

class LoopError(Exception):
    pass

def run(program):
    accumulator = 0
    cursor = 0
    seen = set()
    while cursor < len(program):
        seen.add(cursor)

        operation, argument = program[cursor]
        if operation == 'jmp':
            cursor += argument
        elif operation == 'acc':
            accumulator += argument
            cursor += 1
        elif operation == 'nop':
            cursor += 1

        if cursor in seen:
            raise LoopError(f'loop detected on line #{cursor}')

    return accumulator

swaps = {
    cursor
    for cursor in range(len(program))
    if program[cursor][0] in ('jmp', 'nop')
}

for swap_cursor in swaps:
    operation, argument = program[swap_cursor]
    swapped_operation = 'jmp' if operation == 'nop' else 'nop'
    fixed_program = program[:swap_cursor] + [(swapped_operation, argument)] + program[swap_cursor + 1:]
    try:
        print(run(fixed_program))
        break
    except LoopError:
        continue
