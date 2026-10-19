# maspy-parking

Parking implementation using Maspy

## Run

```bash
make setup
make run
```

`make help` lists all available commands.

## Project structure

```
src/parking/
├── __init__.py          # package exports
├── __main__.py          # entry point (python -m parking)
├── config.py            # DRV_SETTINGS driver profiles
├── environment.py       # Parking environment
├── simulation.py        # main() – wires agents, channel and startup
└── agents/
    ├── __init__.py
    ├── manager.py       # Manager agent
    └── driver.py        # Driver agent
```

## Current version overview

Three actors communicate through the `Parking` channel:

- **Manager** – central agent. Receives spot requests and forwards a `park` goal
  to the requesting driver.
- **Driver** – asks the manager for a spot on startup and parks when it receives
  a `park` goal.
- **Parking** – the environment representing the parking lot. Creates the spots as percepts and controls parking/leaving (`park_spot`, `leave_spot`).

### Flow

1. On startup each `Driver` adds `Goal("ask_spot_available", <manager name>)`.
2. The driver sends `achieve Goal("find_spot_available")` to the manager over the
   `Parking` channel.
3. The manager's `search_empty_spot` plan adds `Goal("SendSpot", <driver>)`.
4. The manager's `send_spot_to_driver` plan picks a free spot and sends `achieve Goal("park", ("Parking", <spot id>))` back.
5. The driver's `park_on_spot` plan parks on the assigned spot, waits, leaves and stops its cycle. If the spot was taken in the meantime, it asks again.

The manager stops its cycle once no `Drv` agents are running.

### Pending improvements

- [ ] Prevent the Manager from offering the same spot to several drivers at once. Today this makes a driver retry because the spot is already occupied when it tries to park.
- [ ] Add a second (and maybe a third) parking environment with different prices.
