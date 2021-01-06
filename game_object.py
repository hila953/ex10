# FILE : ex10.py
# WRITER : Hila Frumer , hila953 , 318933405,
#          Alon Levy , alon153 , 313163958
# EXERCISE : intro2cs1 ex10 2020
# DESCRIPTION: GameObject Object Class
from typing import *


class GameObject:
    """
    This class is the Parent of all object in the game (ship, asteroids,
    torpedoes)
    """
    def __init__(self, loc_x, loc_y, radius, speed_x=0, speed_y=0):
        """
        init
        :param loc_x: the object location's x
        :param loc_y: the object location's y
        :param speed_x: the object speed's x
        :param speed_y: the object speed's y
        """
        self.loc_x: float = loc_x
        self.loc_y: float = loc_y
        self.speed_x: float = speed_x
        self.speed_y: float = speed_y
        self.radius = radius

    def get_speed_x(self) -> float:
        """
        :return: the object speed's x
        """
        return self.speed_x

    def get_radius(self) -> int:
        """
        :return: the objects radius
        """
        return self.radius

    def get_speed_y(self) -> float:
        """
        :return: the object speed's y
        """
        return self.speed_y

    def get_speed(self) -> Tuple[float, float]:
        """
        :return: the object speed
        """
        return self.speed_x, self.speed_y

    def set_speed_x(self, x: float):
        """
        set the object speed's x
        :param x: the object speed's x
        :return: None
        """
        self.speed_x = x

    def set_speed_y(self, y: float):
        """
        set the object speed's y
        :param y: the object speed's y
        :return: None
        """
        self.speed_y = y

    def get_loc_x(self) -> float:
        """
        :return: the object location's x
        """
        return self.loc_x

    def get_loc_y(self) -> float:
        """
        :return: the object location's y
        """
        return self.loc_y

    def set_loc_x(self, x: float):
        """
        set's the objects location's x
        :param x: the objects location's x
        :return: None
        """
        self.loc_x = x

    def set_loc_y(self, y: float):
        """
        set's the objects location's y
        :param y: the objects location's y
        :return: None
        """
        self.loc_y = y

    def set_location(self, x, y):
        """
        set's the objects location
        :param x: the object location's x
        :param y: the object location's y
        :return: None
        """
        self.loc_x = x
        self.loc_y = y

    def get_location(self) -> Tuple[float, float]:
        """
        :return: the object's location
        """
        return self.loc_x, self.loc_y

    def move(self, min_x, max_x, min_y, max_y):
        """
        moves the object
        :param min_x: the minimum x coordinate
        :param max_x: the maximum x coordinate
        :param min_y: the minimum y coordinate
        :param max_y: the maximum y coordinate
        :return: None
        """
        self.loc_x = min_x +\
                    (self.loc_x + self.speed_x - min_x)%\
                    (max_x - min_x)

        self.loc_y = min_y +\
                    (self.loc_y + self.speed_y - min_y)%\
                    (max_y - min_y)
