# FILE : ex10.py
# WRITER : Hila Frumer , hila953 , 318933405,
#          Alon Levy , alon153 , 313163958
# EXERCISE : intro2cs1 ex10 2020
# DESCRIPTION: The main class

from screen import Screen
import sys
import random
from typing import *
from ship import Ship
from game_object import GameObject
from asteroid import Asteroid
from torpedo import Torpedo

# default game variables
MAX_TORPEDOES = 10
DEFAULT_ASTEROIDS_NUM = 5
SCORES = [100, 50, 20]

# different game ending states
END_WIN = 0
END_LOSE = 1
END_QUIT = 2

# dictionary holding messages to display at the end according the the end state
END_MESSAGES = {END_WIN : ("YOU WIN", "Your score is: "),
                END_LOSE : ("YOU LOSE", "You lost all your lives"),
                END_QUIT : ("QUIT", "Goodbye")}


class GameRunner:
    """
    This class hold the game logic and is responsible for the running of the
    game
    """
    def __init__(self, asteroids_amount):
        """
        init
        :param asteroids_amount: the amount of asteroids to start the game
        with
        """
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__ship = self.init_ship() # the player ship
        self.__asteroids = [] # the asteroids in the game
        self.__torpedoes = [] # the torpedoes in the game
        self.init_asteroids(asteroids_amount)
        self.score = 0

    # ------------------------------ INITS ------------------------------
    def init_ship(self):
        """
        creates the ship
        :return the initialized ship
        """
        location = self.get_random_location()
        return Ship(location[0], location[1])

    def init_asteroids(self, amount=DEFAULT_ASTEROIDS_NUM):
        """
        inits the game's asteroids
        :param amount: the number of asteroids to create
        """
        for _ in range(amount):
            location = self.get_random_location()
            while location == self.__ship.get_location():
                location = self.get_random_location()

            asteroid = Asteroid(location[0], location[1])
            self.add_asteroid(asteroid)

    def create_torpedo(self):
        """
        creates a single torpedo and adds to the list
        """
        torpedo = Torpedo(self.__ship.get_loc_x(), self.__ship.get_loc_y(),
                          self.__ship.get_speed_x(), self.__ship.get_speed_y(),
                          self.__ship.get_direction())
        self.__screen.register_torpedo(torpedo)
        self.__torpedoes.append(torpedo)

    # -------------------- MOVEMENT -----------------------------------------
    def move_game_objects(self):
        """
        moves all the game objects
        :return: None
        """
        self.move_object(self.__ship)
        self.move_all_asteroids()
        self.move_all_torpedoes()

    def move_all_torpedoes(self):
        """
        moves all the torpedoes
        :return: None
        """
        for torpedo in self.__torpedoes:
            self.move_object(torpedo)

    def move_all_asteroids(self):
        """
        moves all the asteroids
        :return: None
        """
        for asteroid in self.__asteroids:
            self.move_object(asteroid)

    def move_object(self, obj: GameObject):
        """
        moves a single game object according to the screens dimensions
        :param obj: the object to move
        :return: None
        """
        obj.move(self.__screen_min_x, self.__screen_max_x,
                 self.__screen_min_y, self.__screen_max_y)

    # ------------------------- DRAW ---------------------------------
    def draw_game_objects(self):
        """
        draws all the game objects
        :return: None
        """
        self.__screen.draw_ship(int(self.__ship.get_location()[0]),
                                int(self.__ship.get_location()[1]),
                                self.__ship.get_direction_degrees())

        self.draw_all_asteroids()
        self.draw_all_torpedoes()

    def draw_all_torpedoes(self):
        """
        draws all the torpedoes
        :return: None
        """
        for torpedo in self.__torpedoes:
            self.__screen.draw_torpedo(torpedo, torpedo.get_loc_x(),
                                       torpedo.get_loc_y(),
                                       torpedo.get_direction_degrees())

    def draw_all_asteroids(self):
        """
        draws all the asteroids
        :return: None
        """
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.get_loc_x(),
                                        asteroid.get_loc_y())

    # -------------------- HANDLE GAME OBJECT ----------------------
    def update_torpedoes(self):
        """
        updates all the torpedoes timers and removes torpedoes that ended their
        lifecycle
        :return: None
        """
        for torpedo in self.__torpedoes:
            if torpedo.add_time():
                self.remove_torpedo(torpedo)

    def remove_torpedo(self, torpedo: Torpedo):
        """
        removes a torpedo from the game
        :param torpedo: the torpedo to remove
        :return: None
        """
        self.__screen.unregister_torpedo(torpedo)
        self.__torpedoes.remove(torpedo)

    def remove_asteroid(self, asteroid: Asteroid):
        """
        removes an asteroid from the game
        :param asteroid: the asteroid to remove
        :return: None
        """
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def add_asteroid(self, asteroid):
        """
        adds an asteroid to the game
        :param asteroid: the asteroid to add
        :return: None
        """
        self.__screen.register_asteroid(asteroid, asteroid.get_size())
        self.__asteroids.append(asteroid)

    # -------------------- GENERAL --------------------------
    def check_crashes(self):
        """
        checks if any of the asteroids have hit another game object and handles
        the intersection
        :return: None
        """
        for asteroid in self.__asteroids:
            # handle hitting the ship
            if asteroid.has_intersection(self.__ship):
                self.ship_hit()
                self.remove_asteroid(asteroid)

            for torpedo in self.__torpedoes:
                # handle hitting a torpedo
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
        """
        adds to the player's score according to the asteroid
        :param size_asteroid: the size of the asteroid that was hit
        :return: None
        """
        self.score += SCORES[size_asteroid - 1]
        self.__screen.set_score(self.score)

    def ship_hit(self):
        """
        handles when the ship is hit
        :return: None
        """
        if not self.__ship.hit():
            self.end_game(END_LOSE)
            return
        self.__screen.show_message("HIT!",
                                   f"You have {self.__ship.get_lives()}"
                                   f" lives left")
        self.__screen.remove_life()

    def end_game(self, status):
        """
        ends the game
        :param status: the reason for ending the game
        :return: None
        """
        title, message = END_MESSAGES[status]
        if status == END_WIN:
            message += str(self.score)

        self.__screen.show_message(title, message)
        self.__screen.end_game()
        sys.exit()

    def get_random_location(self):
        """
        generates a random location according to the screens dimensions
        :return: None
        """
        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return x, y

# -------------------- MAIN FUNCTIONS ----------------------
    def run(self):
        """
        runs the game
        :return: None
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        Responsible for running the game loop again and again
        :return: None
        """
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        handles all the game logistics each round
        :return: None
        """
        if self.__screen.should_end():
            self.end_game(END_QUIT)
            return
        self.update_torpedoes()
        self.handle_presses()
        self.move_game_objects()
        self.draw_game_objects()
        self.check_crashes()

    def handle_presses(self):
        """
        handles all the keyboard inputs
        :return: None
        """
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
    """
    the main function. starts the game
    :param amount: amount of asteroids to start the game with
    :return: None
    """
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
