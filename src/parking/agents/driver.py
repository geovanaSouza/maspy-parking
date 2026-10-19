from maspy import *
from time import sleep


class Driver(Agent):
    def __init__(self, agt_name, wait):
        super().__init__(agt_name)
        self.wait_time = wait

    @pl(gain, Goal("ask_spot_available", Any))
    def ask_spot_available_to_manager(self, src, manager):
        self.send(manager, achieve, Goal("find_spot_available"), "Parking")

    @pl(gain, Goal("park",(Any, Any)))
    def park_on_spot(self, src, spot):
        park_environment, spot_id = spot
        self.connect_to(park_environment)
        self.print(f"Parking car from {self.my_name} on spot {spot_id}")
        confirm = self.park_spot(spot_id)
        if confirm is None:
            self.print(f"Spot {spot_id} is unavailable after given by {src}")
            self.add(Goal("ask_spot_available", src))
            return None
        sleep(self.wait_time)
        self.print(f"Leaving spot ({spot_id})")
        self.leave_spot()
        self.disconnect_from(park_environment)
        self.stop_cycle()
