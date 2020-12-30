import math
from game_object import GameObject
TURN_DEGREES = 7
DEFAULT_RADIUS = 1


class Ship(GameObject):

    def __init__(self, loc_x, loc_y, speed_x = 0, speed_y = 0, direction = 0,
                 lives = 3):
        super().__init__(loc_x, loc_y, speed_x, speed_y)
        self.direction: float = direction
        self.lives = lives

    def hit(self):
        self.lives -= 1
        return self.lives

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def get_direction_degrees(self):
        return rad_to_deg(self.direction)

    def turn_right(self):
        self.direction -= deg_to_rad(TURN_DEGREES)
        print(self.direction)

    def turn_left(self):
        self.direction += deg_to_rad(TURN_DEGREES)

    def accelerate(self):
        self.speed_x += math.cos(self.direction)
        self.speed_y += math.sin(self.direction)

    def get_radius(self):
        return DEFAULT_RADIUS


def deg_to_rad(degrees):
    return float(degrees) * math.pi / 180


def rad_to_deg(rad):
    return float(rad) * 180 / math.pi
