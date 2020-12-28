from screen import Screen
import sys
import random
from typing import *
from ship import Ship
from game_object import GameObject
from asteroid import Asteroid
from torpedo import Torpedo


DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__ship = self.init_ship()
        self.__asteroids = []
        self.__torpedoes = []
        self.init_asteroids()


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
        self.move(self.__ship)
        self.move_all_asteroids()
        self.move_all_torpedoes()
        self.__screen.draw_ship(self.__ship.get_location()[0],
                                self.__ship.get_location()[1],
                                self.__ship.get_direction_degrees())
        self.check_crashes()
        self.draw_all_asteroids()
        self.draw_all_torpedoes()

    def draw_all_torpedoes(self):
        for torpedo in self.__torpedoes:
            self.__screen.draw_torpedo(torpedo, torpedo.get_loc_x(),
                                       torpedo.get_loc_y(),
                                       torpedo.get_direction())


    def remove_torpedo(self, torpedo: Torpedo):
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedoes.remove(torpedo)

    def move_all_torpedoes(self):
        for torpedo in self.__torpedoes:
            self.move(torpedo)

    def check_crashes(self):
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                self.ship_hit()
                self.remove_asteroid(asteroid)

            for torpedo in self.__torpedoes:
                if asteroid.has_intersection(torpedo):
                    new_1, new_2 = asteroid.hit(torpedo)
                    self.remove_asteroid(asteroid)
                    if new_1 and new_2:
                        self.add_asteroid(new_1)
                        self.add_asteroid(new_2)
                    self.remove_torpedo(torpedo)

    def ship_hit(self):
        self.__screen.show_message("HIT!",
                                   f"You have {self.__ship.get_lives()}"
                                   f" lives left")
        self.__screen.remove_life()
        self.__ship.hit()

    def remove_asteroid(self, asteroid: Asteroid):
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def move_all_asteroids(self):
        for asteroid in self.__asteroids:
            self.move(asteroid)

    def init_ship(self):
        location = self.get_random_location()
        return Ship(location[0], location[1])

    def draw_all_asteroids(self):
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.get_loc_x(),
                                        asteroid.get_loc_y())

    def get_random_location(self):
        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return x,y


    def get_random_speed(self):
        speed_x = random.choice([i for i in range(-4, 4, 1) if i != 0])
        speed_y = random.choice([i for i in range(-4, 4, 1) if i != 0])
        return speed_x, speed_y

    def init_asteroids(self, amount=DEFAULT_ASTEROIDS_NUM):
        for _ in range(amount):
            location = self.get_random_location()
            while location == self.__ship.get_location():
                location = self.get_random_location()

            speed = self.get_random_speed()
            asteroid = Asteroid(location[0], location[1], speed[0], speed[1])
            self.add_asteroid(asteroid)

    def add_asteroid(self, asteroid):
        self.__screen.register_asteroid(asteroid, asteroid.get_size())
        self.__asteroids.append(asteroid)

    def handle_presses(self):
        if self.__screen.is_left_pressed():
            self.__ship.turn_left()
        if self.__screen.is_right_pressed():
            self.__ship.turn_right()
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
        if self.__screen.is_space_pressed():
            self.create_torpedo()

    def create_torpedo(self):
        torpedo = Torpedo(self.__ship.get_loc_x(), self.__ship.get_loc_y(),
                          self.__ship.get_speed_x(), self.__ship.get_speed_y(),
                          self.__ship.get_direction())
        self.__screen.register_torpedo(torpedo)
        self.__torpedoes.append(torpedo)

    def move(self, obj: GameObject):
        new_x = self.__screen_min_x +\
                    (obj.get_loc_x() + obj.get_speed_x() - self.__screen_min_x)%\
                    (self.__screen_max_x - self.__screen_min_x)

        new_y = self.__screen_min_y +\
                    (obj.get_loc_y() + obj.get_speed_y() - self.__screen_min_y)%\
                    (self.__screen_max_y - self.__screen_min_y)

        obj.set_location(new_x, new_y)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
