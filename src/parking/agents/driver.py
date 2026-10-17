from maspy import *


class Driver(Agent):
    def __init__(self, agt_name):
        super().__init__(agt_name)

    @pl(gain, Goal("ask_spot_available", Any))
    def ask_spot_available_to_manager(self, src, agent):
        self.send(agent, achieve, Goal("find_spot_available"), "Parking")

    @pl(gain, Goal("park"))
    def park_on_spot(self, src):
        self.print(f"Parking car from {self.my_name} on spot available")
        self.stop_cycle()
