from typing import *
import math
from game_object import GameObject
from ship import Ship
DEFAULT_SIZE = 3
import random


class Asteroid(GameObject):

    def __init__(self, loc_x, loc_y, speed_x=-1, speed_y=-1,
                 size=DEFAULT_SIZE):
        if speed_x == -1 or speed_y == -1:
            speed_x, speed_y = get_random_speeds()
        print("creating asteroid with", loc_x, loc_y, speed_x, speed_y)
        super().__init__(loc_x, loc_y, speed_x, speed_y)
        self.size = size

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_radius(self):
        return self.size * 10 - 5

    def has_intersection(self, obj):
        distance = math.sqrt((obj.get_loc_x() - self.loc_x)**2 +
                             (obj.get_loc_y() - self.loc_y)**2)
        return distance <= self.get_radius() + obj.get_radius()

    def hit(self, torpedo):
        if self.size == 1:
            return None, None

        new_speeds = self.new_asteroid_speed(torpedo)
        new_1 = Asteroid(self.loc_x, self.loc_y, new_speeds[0], new_speeds[1],
                         self.size-1)
        new_2 = Asteroid(self.loc_x, self.loc_y, new_speeds[2], new_speeds[3],
                         self.size - 1)
        return new_1, new_2

    def new_asteroid_speed(self, torpedo):
        new_speed_x = (torpedo.speed_x + self.speed_x) / \
                      math.sqrt(self.speed_x**2 + self.speed_y**2)

        new_speed_y = (torpedo.speed_y + self.speed_y) / \
                      math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)

        return new_speed_x, new_speed_y, (-1)*new_speed_x, (-1)*new_speed_y


def get_random_speeds():
    speed_x = random.choice([i for i in range(-4, 4, 1) if i != 0])
    speed_y = random.choice([i for i in range(-4, 4, 1) if i != 0])
    return speed_x, speed_y
