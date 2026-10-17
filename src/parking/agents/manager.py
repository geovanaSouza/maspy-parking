from maspy import *


class Manager(Agent):
    def on_idle(self):
        if Admin().running_class_agents("Drv") is False:
            self.stop_cycle()

    @pl(gain, Goal("find_spot_available"))
    def search_empty_spot(self, src):
        self.print("Searching for spots empty")
        self.add(Goal("SendSpot", src))

    @pl(gain, Goal("SendSpot", Any))
    def send_spot_to_driver(self, src, agent):
        self.print(f"Sending spot available to {agent}")
        self.send(agent, achieve, Goal("park"), "Parking")
