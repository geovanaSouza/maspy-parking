from maspy import *

class Parking(Environment):
    def __init__(self, env_name, nr_spots=10):
        super().__init__(env_name)

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
        self.send(agent,achieve,Goal("park"), "Parking")

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

def main(num_driver_agents: int = 10, num_spots: int = 5):
    print(f"Initializing {num_driver_agents} agents in an environment with {num_spots} spots")

    # Define environment
    park = Parking('Parking', num_spots)

    # Define communication channel
    park_ch = Channel("Parking")

    # Define Manager Agent
    manager = Manager()
    manager.add(Goal("find_spot_available"))

    drv_settings: dict = {"budget": [(10,12),(8,14),(10,20),(12,14),(12,16)],
                          "counter": [0.4, 0.8, 1, 1.2, 1.4],
                          "wait": [0, 0.5, 0.7, 1, 1.5]}
    driver_list: list = []

    for i in range(num_driver_agents):
        # Assign budget, counter and wait from drv_settings to each driver agent
        budget = drv_settings["budget"][i%len(drv_settings["budget"])]
        print(f"Budget from driver {i}: {budget}")
        counter = drv_settings["counter"][(i*2)%5]
        print(f"Counter from driver {i}: {counter}")
        print()
        drv = Driver("Drv")
        drv.add(Goal("ask_spot_available", manager.my_name))
        driver_list.append(drv)
        

    # Configure admin and system initialization
    Admin(file_log=True)
    Admin().connect_to(manager, park_ch)
    Admin().connect_to(driver_list, park_ch)
    Admin().start_system()

if __name__ == "__main__":
    main(50, 10)