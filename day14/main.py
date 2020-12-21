import fileinput
from itertools import chain

_memory = {}

def apply_mask(value, mask):
    bits = [
        bit if override == 'X' else override
        for (override, bit) in zip(mask, list(bin(value)[2:].zfill(36)))
    ]
    return int(''.join(bits), 2)

def assign(address, value, mask):
    _memory[address] = apply_mask(value, mask)


def gen_part2(mask):
    if mask == '1' or mask == '0':
        return [mask]
    elif mask == 'X':
        return ['0', '1']
    else:
        first_char = mask[0]
        if first_char == '0' or first_char == '1':
            return (f'{mask[0]}{generation}' for generation in gen_part2(mask[1:]))
        elif first_char == 'X':
            return chain(
                (f'0{generation}' for generation in gen_part2(mask[1:])),
                (f'1{generation}' for generation in gen_part2(mask[1:])),
            )
        else:
            raise ValueError(f'mask "{mask}" cannot be handled')

def apply_mask_part_2(address, mask):
    bits = [
        bit if override == '0' else ('1' if override == '1' else 'X')
        for (override, bit) in zip(mask, list(bin(address)[2:].zfill(36)))
    ]
    return gen_part2(''.join(bits))

def assign_part_2(address, value, mask):
    for address in apply_mask_part_2(address, mask):
        _memory[address] = value

current_mask = None
for command, value in [line.strip().split(' = ') for line in fileinput.input()]:
    if command == 'mask':
        current_mask = list(value)
    else: # mem
        address = int(command[4:-1])
        value = int(value)
        assign_part_2(address, value, current_mask)

print(sum(value for value in _memory.values()))
