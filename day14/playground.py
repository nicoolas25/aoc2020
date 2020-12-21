import unittest
from itertools import chain

def generate(mask):
    if mask == '1' or mask == '0':
        return [mask]
    elif mask == 'X':
        return ['0', '1']
    else:
        first_char = mask[0]
        if first_char == '0' or first_char == '1':
            return (f'{mask[0]}{generation}' for generation in generate(mask[1:]))
        elif first_char == 'X':
            return chain(
                (f'0{generation}' for generation in generate(mask[1:])),
                (f'1{generation}' for generation in generate(mask[1:])),
            )
        else:
            raise ValueError(f'mask "{mask}" cannot be handled')

class TestGenerateMethods(unittest.TestCase):
    def test_generate(self):
        self.assertEqual(['0'], list(generate('0')))
        self.assertEqual(['1'], list(generate('1')))
        self.assertEqual(['0', '1'], list(generate('X')))
        self.assertEqual(['01', '11'], list(generate('X1')))
        self.assertEqual(['010', '011', '110', '111'], list(generate('X1X')))

if __name__ == '__main__':
    unittest.main()
