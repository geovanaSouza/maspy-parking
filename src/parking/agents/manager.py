from maspy import *


class Manager(Agent):
    def on_idle(self):
        if Admin().running_class_agents("Drv") is False:
            self.stop_cycle()

    @pl(gain, Goal("find_spot_available"))
    def search_empty_spot(self, src):
        self.print("Searching for spots empty")
        self.add(Goal("SendSpot", src), True)

    @pl(gain, Goal("SendSpot", Any), Belief("spot",(Any, "free"),"Parking"))
    def send_spot_to_driver(self, src, agent, spot):
        spot_number, spot_status = spot
        self.print(f"Sending spot {spot_number} available to {agent}")
        self.send(agent, achieve, Goal("park", ("Parking", spot_number)), "Parking")
