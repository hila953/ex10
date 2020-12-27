from screen import Screen
import sys
import random
from ship import Ship

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__ship = self.init_ship()



    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        self.handle_presses()
        self.__ship.move(self.__screen_min_x, self.__screen_max_x,
                         self.__screen_min_y, self.__screen_max_y)
        self.__screen.draw_ship(self.__ship.get_location()[0],
                                self.__ship.get_location()[1],
                                self.__ship.get_direction())

    def init_ship(self):
        loc_x = random.randint(self.__screen_min_x, self.__screen_max_x)
        loc_y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return Ship(loc_x, loc_y)

    def handle_presses(self):
        if self.__screen.is_left_pressed():
            self.__ship.turn_left()
        if self.__screen.is_right_pressed():
            self.__ship.turn_right()
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
            # self.__ship.move(self.__screen_min_x, self.__screen_max_x,
            #                  self.__screen_min_y, self.__screen_max_y)





def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
