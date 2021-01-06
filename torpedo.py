# FILE : ex10.py
# WRITER : Hila Frumer , hila953 , 318933405,
#          Alon Levy , alon153 , 313163958
# EXERCISE : intro2cs1 ex10 2020
# DESCRIPTION: Torpedo Object Class

from game_object import GameObject
import math

DEFAULT_RADIUS = 4


class Torpedo(GameObject):
    """
    This class represents the torpedo of the game
    Child class of GameObject
    """
    def __init__(self, loc_x, loc_y, ship_speed_x=0, ship_speed_y=0,
                 ship_direction=0):
        """
        init
        :param loc_x: the starting location's x
        :param loc_y: the starting location's y
        :param speed_x: the starting speed's x
        :param speed_y: the starting speed's y
        :param direction: the starting direction
        """
        self.direction = ship_direction
        speed_x, speed_y = self.calc_speed(ship_speed_x, ship_speed_y)
        super().__init__(loc_x, loc_y, DEFAULT_RADIUS, speed_x, speed_y)
        self.time = 0

    def add_time(self) -> bool:
        """
        adds another count to the torpedo's timer
        :return: True if the torpedo finished its lifecycle, False otherwise
        """
        self.time += 1
        return self.time == 200

    def calc_speed(self, ship_speed_x, ship_speed_y):
        """
        calculates the torpedo's speed according to the ship's speed
        :param ship_speed_x: the ship speed's x
        :param ship_speed_y: the ship speed's y
        :return: None
        """
        x = ship_speed_x + 2 * math.cos(self.direction)
        y = ship_speed_y + 2 * math.sin(self.direction)
        return x, y

    def get_direction(self):
        """
        :return: the torpedo's direction in radians
        """
        return self.direction

    def set_direction(self, direction):
        """
        sets the torpedo's direction
        :param direction: the direction to set
        :return: None
        """
        self.direction = direction

    def get_direction_degrees(self):
        """
        :return: the torpedo's direction in degrees
        """
        return rad_to_deg(self.direction)


def rad_to_deg(rad):
    """
    converts radians to degrees
    :param rad: radians to convert
    :return: the angle in degrees
    """
    return float(rad) * 180 / math.pi