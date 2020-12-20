import unittest

def rotate_right(x, y, angle, ox=0, oy=0):
    if angle == 270:
        x, y = rotate(x, y, 180, ox, oy)
        return rotate(x, y, 90, ox, oy)

    if angle == 180:
        x, y = rotate(x, y, 90, ox, oy)
        return rotate(x, y, 90, ox, oy)

    if angle == 90:
        return (y - oy + ox, -(x - ox) + oy)
    else:
        raise ValueError(f'Unahandled angle {angle}')

def rotate_left(x, y, angle, ox=0, oy=0):
    if angle == 270:
        x, y = rotate(x, y, 180, ox, oy)
        return rotate(x, y, 90, ox, oy)

    if angle == 180:
        x, y = rotate(x, y, 90, ox, oy)
        return rotate(x, y, 90, ox, oy)

    if angle == 90:
        return (-(y - oy) + ox, x - ox + oy)
    else:
        raise ValueError(f'Unahandled angle {angle}')

class TestRotateMethods(unittest.TestCase):
    def test_rotate_right(self):
        # Using origin
        self.assertEqual((5, -1), rotate_right(1, 5, 90))
        self.assertEqual((-1, -5), rotate_right(5, -1, 90))
        self.assertEqual((-5, 1), rotate_right(-1, -5, 90))
        self.assertEqual((1, 5), rotate_right(-5, 1, 90))

        # Using a different reference
        self.assertEqual((5, 1), rotate_right(1, 5, 90, 1, 1))
        self.assertEqual((1, -3), rotate_right(5, 1, 90, 1, 1))
        self.assertEqual((-3, 1), rotate_right(1, -3, 90, 1, 1))
        self.assertEqual((1, 5), rotate_right(-3, 1, 90, 1, 1))

    def test_rotate_left(self):
        # Using origin
        self.assertEqual((-5, 1), rotate_left(1, 5, 90))
        self.assertEqual((-1, -5), rotate_left(-5, 1, 90))
        self.assertEqual((5, -1), rotate_left(-1, -5, 90))
        self.assertEqual((1, 5), rotate_left(5, -1, 90))

        # Using a different reference
        self.assertEqual((-3, 1), rotate_left(1, 5, 90, 1, 1))
        self.assertEqual((1, -3), rotate_left(-3, 1, 90, 1, 1))
        self.assertEqual((5, 1), rotate_left(1, -3, 90, 1, 1))
        self.assertEqual((1, 5), rotate_left(5, 1, 90, 1, 1))

if __name__ == '__main__':
    unittest.main()

