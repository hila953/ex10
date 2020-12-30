class GameObject:

    def __init__(self, loc_x, loc_y, speed_x=0, speed_y=0):
        self.loc_x: float = loc_x
        self.loc_y: float = loc_y
        self.speed_x: float = speed_x
        self.speed_y: float = speed_y

    def get_speed_x(self):
        return self.speed_x

    def get_speed_y(self):
        return self.speed_y

    def get_speed(self):
        return self.speed_x, self.speed_y

    def set_speed_x(self, x):
        self.speed_x = x

    def set_speed_y(self, y):
        self.speed_y = y

    def get_loc_x(self):
        return self.loc_x

    def get_loc_y(self):
        return self.loc_y

    def set_loc_x(self, x):
        self.loc_x = x

    def set_loc_y(self, y):
        self.loc_y = y

    def set_location(self, x, y):
        self.loc_x = x
        self.loc_y = y

    def get_location(self):
        return self.loc_x, self.loc_y


    def move(self, min_x, max_x, min_y, max_y):
        self.loc_x = min_x +\
                    (self.loc_x + self.speed_x - min_x)%\
                    (max_x - min_x)

        self.loc_y = min_y +\
                    (self.loc_y + self.speed_y - min_y)%\
                    (max_y - min_y)
