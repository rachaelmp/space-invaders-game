from vector import Vector


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = 30, 30, 50

        self.ship_speed_factor = 8
        self.ship_limit = 3

        self.alien_speed_factor = 3
        self.fleet_drop_speed = 5
        self.fleet_direction = Vector(1, 0)
        self.alien_fire_chance = 1

        self.laser_speed_factor = 8
        self.laser_width = 3
        self.laser_height = 20
        self.laser_color = 255, 40, 40

    def increase_difficulty(self, increase_by):
        self.alien_speed_factor += increase_by
        self.fleet_drop_speed += increase_by
        self.alien_fire_chance += increase_by

    def reset_difficulty(self):
        self.alien_speed_factor = 3
        self.fleet_drop_speed = 5
        self.alien_fire_chance = 1

