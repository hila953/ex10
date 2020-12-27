import math
TURN_DEGREES = 7


class Ship:

    def __init__(self, loc_x, loc_y, speed_x = 0, speed_y = 0, direction = 0):
        self.__loc_x: float= loc_x
        self.__loc_y: float = loc_y
        self.__speed_x: float = speed_x
        self.__speed_y: float = speed_y
        self.__direction = direction

    def get_loc_x(self):
        return self.__loc_x

    def get_loc_y(self):
        return self.__loc_y

    def move(self, min_x, max_x, min_y, max_y):
        self.__loc_x = min_x +\
                    (self.__loc_x + self.__speed_x - min_x)%\
                    (max_x - min_x)

        self.__loc_y = min_y +\
                    (self.__loc_y + self.__speed_y - min_y)%\
                    (max_y - min_y)

    def get_location(self):
        return self.__loc_x, self.__loc_y

    def get_direction(self):
        return self.__direction

    def turn_right(self):
        self.__direction -= TURN_DEGREES

    def turn_left(self):
        self.__direction += TURN_DEGREES

    def accelerate(self):
        radians = deg_to_rad(self.__direction)
        self.__speed_x += math.cos(radians)
        self.__speed_y += math.sin(radians)


def deg_to_rad(degrees):
    return degrees * math.pi / 180