from maspy import *


class Manager(Agent):
    def __init__(self, agt_name = None):
        super().__init__(agt_name, read_all_mail=True)
        self.add(Belief("spotPrice",15,adds_event=False))
        self.add(Belief("minPrice",10,adds_event=False))
        self.add(Goal("broadcast_price"))
        self.print("Manager initialized")
    
    def on_idle(self):
        if Admin().running_class_agents("Drv") is False:
            self.stop_cycle()

    @pl(gain, Goal("broadcast_price"), Belief("spotPrice", Any))
    def send_price(self, src, spot_price):
        self.print(f"Broadcast spot price[{spot_price}] to all Agents in Parking Channel.")
        self.send(broadcast,achieve,Goal("checkPrice", (spot_price)), "Parking")

    @pl(gain, Goal("analyze_offer", (Any, Any)), Belief("minPrice", Any))
    def analyze_offer(self, src, offer_answer, min_price):
        answer, price = offer_answer
        self.print(f"Received offer {offer_answer} from {src}")
        match answer:
            case "reject":
                self.print(f"Given price [{price}] rejected by {src}")
                pass
            case "accept":
                self.print(f"Price accepted [{price}] by {src}. Choosing spot.")
                self.add(Goal("SendSpot", src), True)
            case "offer":
                if price < min_price:
                    count_offer = (min_price+price)/1.8
                    count_offer = round(count_offer,2)
                    self.print(f"Price offered [{price}] from {src} too low. Counter-offer [{count_offer}]")
                    self.send(src, achieve, Goal("checkPrice", count_offer), "Parking")
                else:
                    self.print(f"Offered price from {src} accepted [{price}]. Choosing spot.")
                    self.add(Goal("SendSpot", src), True)

    @pl(gain, Goal("SendSpot", Any), Belief("spot",(Any, "free"),"Parking"))
    def send_spot_to_driver(self, src, agent, spot):
        spot_number, spot_status = spot
        self.print(f"Sending spot {spot_number} available to {agent}")
        self.send(agent, achieve, Goal("park", ("Parking", spot_number)), "Parking")
