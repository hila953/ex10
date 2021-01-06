# FILE : ex10.py
# WRITER : Hila Frumer , hila953 , 318933405,
#          Alon Levy , alon153 , 313163958
# EXERCISE : intro2cs1 ex10 2020
# DESCRIPTION: Ship Object Class

import math
from game_object import GameObject

# Constants for the ship
TURN_DEGREES = 7
DEFAULT_RADIUS = 1
STARTING_LIVES = 3


class Ship(GameObject):
    """
    This class represents the ship of the game
    Child class of GameObject
    """

    def __init__(self, loc_x, loc_y, speed_x = 0, speed_y = 0,
                 direction = 0,
                 lives = STARTING_LIVES):
        """
        init
        :param loc_x: the starting location's x
        :param loc_y: the starting location's y
        :param speed_x: the starting speed's x
        :param speed_y: the starting speed's y
        :param direction: the starting direction
        :param lives: the amount of lives the ship starts with
        """
        super().__init__(loc_x, loc_y, DEFAULT_RADIUS, speed_x, speed_y)
        self.direction: float = direction
        self.lives = lives

    def hit(self) -> int:
        """
        reduces a single life
        :return: the live's remaining
        """
        self.lives -= 1
        return self.lives

    def get_lives(self) -> int:
        """
        :return: the ship's lives
        """
        return self.lives

    def set_lives(self, lives: int):
        """
        set the ships lives
        :param lives: live to set
        :return: None
        """
        self.lives = lives

    def get_direction(self):
        """
        :return: the ship's direction in radians
        """
        return self.direction

    def set_direction(self, direction: float):
        """
        set the ships direction in radians
        :param direction: the direction to set
        :return: None
        """
        self.direction = direction

    def get_direction_degrees(self) -> float:
        """
        :return: the ship's direction in degrees
        """
        return rad_to_deg(self.direction)

    def turn_right(self):
        """
        turns the ship right
        :return: None
        """
        self.direction -= deg_to_rad(TURN_DEGREES)

    def turn_left(self):
        """
        turns the ship left
        :return: None
        """
        self.direction += deg_to_rad(TURN_DEGREES)

    def accelerate(self):
        """
        raises the ship's speed according to its direction
        :return: None
        """
        self.speed_x += math.cos(self.direction)
        self.speed_y += math.sin(self.direction)


def deg_to_rad(degrees: int) -> float:
    """
    converts degrees to radians
    :param degrees: the degrees to convert
    :return: the angle in radians
    """
    return float(degrees) * math.pi / 180


def rad_to_deg(rad: float) -> float:
    """
    converts radians to degrees
    :param rad: radians to convert
    :return: the angle in degrees
    """
    return rad * 180 / math.pi
