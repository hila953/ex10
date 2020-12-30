from screen import Screen
import sys
import random
from typing import *
from ship import Ship
from game_object import GameObject
from asteroid import Asteroid
from torpedo import Torpedo

MAX_TORPEDOES = 10
DEFAULT_ASTEROIDS_NUM = 5
SCORES = [100, 50, 20]

END_WIN = 0
END_LOSE = 1
END_QUIT = 2

END_MESSAGES = {END_WIN : ("YOU WIN", "Your score is: "),
                END_LOSE : ("YOU LOSE", "You lost all your lives"),
                END_QUIT : ("QUIT", "Goodbye")}


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        # init game pieces
        self.__ship = self.init_ship()
        self.__asteroids = []
        self.__torpedoes = []
        self.init_asteroids(asteroids_amount)
        self.score = 0

    # ------------------------------ INITS ------------------------------
    def init_ship(self):
        location = self.get_random_location()
        return Ship(location[0], location[1])

    def init_asteroids(self, amount=DEFAULT_ASTEROIDS_NUM):
        for _ in range(amount):
            location = self.get_random_location()
            while location == self.__ship.get_location():
                location = self.get_random_location()

            asteroid = Asteroid(location[0], location[1])
            self.add_asteroid(asteroid)

    def create_torpedo(self):
        torpedo = Torpedo(self.__ship.get_loc_x(), self.__ship.get_loc_y(),
                          self.__ship.get_speed_x(), self.__ship.get_speed_y(),
                          self.__ship.get_direction())
        self.__screen.register_torpedo(torpedo)
        self.__torpedoes.append(torpedo)

    # -------------------- MOVEMENT -----------------------------------------
    def move_game_objects(self):
        self.move_object(self.__ship)
        self.move_all_asteroids()
        self.move_all_torpedoes()

    def move_all_torpedoes(self):
        for torpedo in self.__torpedoes:
            self.move_object(torpedo)

    def move_all_asteroids(self):
        for asteroid in self.__asteroids:
            self.move_object(asteroid)

    def move_object(self, obj: GameObject):
        obj.move(self.__screen_min_x, self.__screen_max_x,
                 self.__screen_min_y, self.__screen_max_y)

    # ------------------------- DRAW ---------------------------------
    def draw_game_objects(self):
        self.__screen.draw_ship(self.__ship.get_location()[0],
                                self.__ship.get_location()[1],
                                self.__ship.get_direction_degrees())

        self.draw_all_asteroids()
        self.draw_all_torpedoes()

    def draw_all_torpedoes(self):
        for torpedo in self.__torpedoes:
            self.__screen.draw_torpedo(torpedo, torpedo.get_loc_x(),
                                       torpedo.get_loc_y(),
                                       torpedo.get_direction_degrees())

    def draw_all_asteroids(self):
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.get_loc_x(),
                                        asteroid.get_loc_y())

    # -------------------- HANDLE GAME OBJECT ----------------------
    def update_torpedoes(self):
        for torpedo in self.__torpedoes:
            if torpedo.add_time():
                self.remove_torpedo(torpedo)

    def remove_torpedo(self, torpedo: Torpedo):
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedoes.remove(torpedo)

    def remove_asteroid(self, asteroid: Asteroid):
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def add_asteroid(self, asteroid):
        self.__screen.register_asteroid(asteroid, asteroid.get_size())
        self.__asteroids.append(asteroid)

    # -------------------- GENERAL --------------------------
    def check_crashes(self):
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                self.ship_hit()
                self.remove_asteroid(asteroid)

            for torpedo in self.__torpedoes:
                if asteroid.has_intersection(torpedo):
                    self.add_score(asteroid.get_size())
                    new_1, new_2 = asteroid.hit(torpedo)
                    self.remove_asteroid(asteroid)
                    if new_1 and new_2:
                        self.add_asteroid(new_1)
                        self.add_asteroid(new_2)

                    self.remove_torpedo(torpedo)
                    if not self.__asteroids:
                        self.end_game(END_WIN)

    def add_score(self, size_asteroid):
        self.score += SCORES[size_asteroid - 1]
        self.__screen.set_score(self.score)

    def ship_hit(self):
        if not self.__ship.hit():
            self.end_game(END_LOSE)
            return
        self.__screen.show_message("HIT!",
                                   f"You have {self.__ship.get_lives()}"
                                   f" lives left")
        self.__screen.remove_life()

    def end_game(self, status):
        title, message = END_MESSAGES[status]
        if status == END_WIN:
            message += str(self.score)

        self.__screen.show_message(title, message)
        self.__screen.end_game()
        sys.exit()

    def get_random_location(self):
        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return x, y

# -------------------- MAIN FUNCTIONS ----------------------
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
        if self.__screen.should_end():
            self.end_game(END_QUIT)
            return
        self.update_torpedoes()
        self.handle_presses()
        self.move_game_objects()
        self.draw_game_objects()
        self.check_crashes()

    def handle_presses(self):
        if self.__screen.is_left_pressed():
            self.__ship.turn_left()
        if self.__screen.is_right_pressed():
            self.__ship.turn_right()
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
        if self.__screen.is_space_pressed():
            if len(self.__torpedoes) < MAX_TORPEDOES:
                self.create_torpedo()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
