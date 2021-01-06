# FILE : ex10.py
# WRITER : Hila Frumer , hila953 , 318933405,
#          Alon Levy , alon153 , 313163958
# EXERCISE : intro2cs1 ex10 2020
# DESCRIPTION: Asteroid Object Class

from typing import *
import math
from game_object import GameObject
from ship import Ship
from torpedo import Torpedo
import random

# default asteroid size and speed
DEFAULT_SIZE = 3
MAX_SPEED = 4
MIN_SPEED = 1


class Asteroid(GameObject):
    """
    This class represents the asteroids of the game
    Child class of GameObject
    """
    def __init__(self, loc_x, loc_y, speed_x=-1, speed_y=-1,
                 size=DEFAULT_SIZE):
        """
        init
        :param loc_x: the starting location's x
        :param loc_y: the starting location's y
        :param speed_x: the starting speed's x
        :param speed_y: the starting speed's y
        :param size: the starting size
        """
        if speed_x == -1 or speed_y == -1:
            speed_x, speed_y = get_random_speeds()
        super().__init__(loc_x, loc_y, size * 10 - 5, speed_x, speed_y)
        self.size = size

    def get_size(self) -> int:
        """
        :return: the asteroid's size
        """
        return self.size

    def set_size(self, size: int):
        """
        set the asteroid's size
        :param size: the size
        :return: None
        """
        self.size = size

    def has_intersection(self, obj: GameObject) -> bool:
        """
        checks if the asteroid has an intersection with another game object
        :param obj: the object to check intersection with
        :return: True if the is an intersection, False otherwise
        """
        distance = math.sqrt((obj.get_loc_x() - self.loc_x)**2 +
                             (obj.get_loc_y() - self.loc_y)**2)
        return distance <= self.get_radius() + obj.get_radius()

    def hit(self, torpedo: Torpedo):
        """
        handles a hit from a torpedo
        :param torpedo: the torpedo that hit the asteroid
        :return: two new smaller asteroids in case size>1, None,None otherwise
        """
        if self.size == 1:
            return None, None

        new_speeds = self.new_asteroid_speed(torpedo)
        new_1 = Asteroid(self.loc_x, self.loc_y, new_speeds[0], new_speeds[1],
                         self.size-1)
        new_2 = Asteroid(self.loc_x, self.loc_y, new_speeds[2], new_speeds[3],
                         self.size - 1)
        return new_1, new_2

    def new_asteroid_speed(self, torpedo):
        """
        calculates the speeds of the two new asteroids according to the
        speed of the
        torpedo that hit it
        :param torpedo: the torpedo
        :return: a tuple containing the speeds of the new asteroids
        """
        new_speed_x = (torpedo.speed_x + self.speed_x) / \
                      math.sqrt(self.speed_x**2 + self.speed_y**2)

        new_speed_y = (torpedo.speed_y + self.speed_y) / \
                      math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)

        return new_speed_x, new_speed_y, (-1)*new_speed_x, (-1)*new_speed_y


def get_random_speeds():
    """
    creates a random speed for a new asteroid
    :return: a tuple with the speed's x and y
    """
    speed_x = random.choice([i for i in range(-1 * MAX_SPEED, MAX_SPEED,
                                              MIN_SPEED) if i != 0])
    speed_y = random.choice([i for i in range(-1 * MAX_SPEED, MAX_SPEED,
                                              MIN_SPEED) if i !=0])
    return speed_x, speed_y
