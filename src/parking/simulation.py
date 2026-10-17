from maspy import *

from parking.agents.driver import Driver
from parking.agents.manager import Manager
from parking.config import DRV_SETTINGS
from parking.environment import Parking


def main(num_driver_agents: int = 10, num_spots: int = 5):
    print(f"Initializing {num_driver_agents} agents in an environment with {num_spots} spots")

    # Define environment
    park = Parking('Parking', num_spots)

    # Define communication channel
    park_ch = Channel("Parking")

    # Define Manager Agent
    manager = Manager()
    manager.add(Goal("find_spot_available"))

    driver_list: list = []

    for i in range(num_driver_agents):
        # Assign budget, counter and wait from DRV_SETTINGS to each driver agent
        budget = DRV_SETTINGS["budget"][i % len(DRV_SETTINGS["budget"])]
        print(f"Budget from driver {i}: {budget}")
        counter = DRV_SETTINGS["counter"][(i * 2) % 5]
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
