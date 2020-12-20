import fileinput
from enum import Enum

class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'

class Orientation(Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'

def rotator_90(original_fn):
    def decorated_fn(x, y, angle, ox=0, oy=0):
        if angle == 270:
            x, y = decorated_fn(x, y, 180, ox, oy)
            return decorated_fn(x, y, 90, ox, oy)

        if angle == 180:
            x, y = decorated_fn(x, y, 90, ox, oy)
            return decorated_fn(x, y, 90, ox, oy)

        if angle == 90:
            dx, dy = x - ox, y - oy
            x, y = original_fn(dx, dy)
            return (x + ox, y + oy)
        else:
            raise ValueError(f'Unahandled angle {angle}')
    return decorated_fn


@rotator_90
def rotate_right(x, y):
        return (y, -x)

@rotator_90
def rotate_left(x, y):
    return (-y, x)

_movements = {
    Orientation.NORTH: (0, 1),
    Orientation.EAST: (1, 0),
    Orientation.SOUTH: (0, -1),
    Orientation.WEST: (-1, 0),
}

class Simulation:
    def __init__(self):
        self.ship_x = 0
        self.ship_y = 0
        self.waypoint_x = 10
        self.waypoint_y = 1

    def rotate_waypoint(self, direction, angle):
        rotate_fn = rotate_left if direction == Direction.LEFT else rotate_right
        self.waypoint_x, self.waypoint_y = rotate_fn(
            x=self.waypoint_x,
            y=self.waypoint_y,
            angle=angle,
            ox=self.ship_x,
            oy=self.ship_y,
        )

    def move_waypoint(self, orientation, amount):
        dx, dy = _movements[orientation]
        self.waypoint_x = self.waypoint_x + (amount * dx)
        self.waypoint_y = self.waypoint_y + (amount * dy)

    def move_ship_to_waypoint(self):
        dx, dy = self.waypoint_x - self.ship_x, self.waypoint_y - self.ship_y
        self.ship_x, self.ship_y = self.waypoint_x, self.waypoint_y
        self.waypoint_x, self.waypoint_y = self.ship_x + dx, self.ship_y + dy

simulation = Simulation()
for command in (line.strip() for line in fileinput.input()):
    letter, number = command[0:1], int(command[1:])
    if letter == 'F':
        for _ in range(number):
            simulation.move_ship_to_waypoint()
    elif letter == 'N' or letter == 'S' or letter == 'E' or letter == 'W':
        simulation.move_waypoint(
            orientation=Orientation(letter),
            amount=number,
        )
    elif letter == 'L' or letter == 'R':
        simulation.rotate_waypoint(
            direction=Direction(letter),
            angle=number,
        )
    else:
        raise ValueError(f'Unsupported command: "{letter}"')


print(abs(simulation.ship_x) + abs(simulation.ship_y))
