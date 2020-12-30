from game_object import GameObject
import math

DEFAULT_RADIUS = 4


class Torpedo(GameObject):
    def __init__(self, loc_x, loc_y, ship_speed_x=0, ship_speed_y=0,
                 ship_direction=0):
        self.direction = ship_direction
        speed_x, speed_y = self.calc_speed(ship_speed_x, ship_speed_y)
        super().__init__(loc_x, loc_y, speed_x, speed_y)
        self.time = 0

    def add_time(self) -> bool:
        self.time += 1
        return self.time == 200

    def calc_speed(self, ship_speed_x, ship_speed_y):
        x = ship_speed_x + 2 * math.cos(self.direction)
        y = ship_speed_y + 2 * math.sin(self.direction)
        return x, y

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def get_radius(self):
        return DEFAULT_RADIUS

    def get_direction_degrees(self):
        return rad_to_deg(self.direction)


def rad_to_deg(rad):
    return float(rad) * 180 / math.pi