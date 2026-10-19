from maspy import *


class Parking(Environment):
    def __init__(self, env_name, nr_spots=10):
        super().__init__(env_name)
        self.print(f"Starting parking with {nr_spots} spots")
        for n in range(1,nr_spots+1):
            self.create(Percept("spot",(n,"free"),"Spots",False))

    def park_spot(self, agt, spot_id):
        spot = self.get(Percept("spot",(spot_id,Any)))
        if spot is None:
            self.print(f"Spot ({spot_id}) does not exist")
            return None
        status = spot.values[1]
        if status == "free":
            self.print(f"Driver {agt} parking on spot ({spot_id})")
            self.change(spot, values=(spot_id,[agt]))
            return spot.values
        self.print(f"Requested spot ({spot_id}) unavailable, allocated to {status}")
        return None

    def leave_spot(self, agt):
        spot = self.get(Percept("spot",(Any,[agt])))
        if spot is None:
            self.print(f"Agent {agt} is not allocated to any spots")
            return None
        spot_id = spot.values[0]
        self.print(f"Driver {agt} leaving spot {spot_id}")
        self.change(spot, values=(spot_id,"free"))
