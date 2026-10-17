from maspy import *


class Parking(Environment):
    def __init__(self, env_name, nr_spots=10):
        super().__init__(env_name)
