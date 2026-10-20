from maspy import *
import random as rnd
from time import sleep


class Driver(Agent):
    def __init__(self, agt_name, budget, counter, wait):
        super().__init__(agt_name)
        self.counter = counter
        self.wait_time = wait
        self.last_price = 0
        self.add(Belief("budget",budget,adds_event=False))

    @pl(gain, Goal("checkPrice", (Any)), Belief("budget", (Any, Any)))
    def check_price(self, src, given_price, budget):
        self.wait(rnd.random()*2)
        want_price, max_price = budget
        if self.last_price == given_price:
            self.print(f"Rejecting price [{given_price}]. Same as last offer")
            answer = ("reject", given_price)
        elif given_price > 2*max_price:
            self.print(f"Rejecting price [{given_price}]. Too Higher than my max [{max_price}]")
            answer = ("reject", given_price)
        elif given_price <= want_price:
            self.print(f"Accepting price [{given_price}]. Wanted [{want_price}]")
            answer = ("accept", given_price)
        else:
            counter_offer = (want_price+given_price)/(self.counter+1.5)
            counter_offer = round(counter_offer,2)
            self.print(f"Making counter-offer for price [{given_price}]. Offering[{counter_offer}]")
            answer = ("offer", counter_offer)

        if answer[0] == "reject":
            self.stop_cycle()
        else:
            self.send(src, achieve, Goal("analyze_offer", answer), "Parking")
            self.last_price = given_price

    @pl(gain, Goal("park",(Any, Any)))
    def park_on_spot(self, src, spot):
        park_environment, spot_id = spot
        self.connect_to(park_environment)
        self.print(f"Parking car from {self.my_name} on spot {spot_id}")
        confirm = self.park_spot(spot_id)
        if confirm is None:
            self.print(f"Spot {spot_id} is unavailable after given by {src}")
            self.send(src, achieve, Goal("SendSpot", self.my_name), "Parking")
            return None
        sleep(self.wait_time)
        self.print(f"Leaving spot ({spot_id})")
        self.leave_spot()
        self.disconnect_from(park_environment)
        self.stop_cycle()
