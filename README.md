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

- [ ] Offer each spot to only one driver at a time, keeping it reserved until the driver parks or gives up. Today several drivers can receive the same spot and end up retrying because it is already occupied.
- [ ] When all spots are occupied, keep the waiting drivers in a queue and serve them in order as spots are freed, instead of leaving their requests unanswered.
- [ ] Make sure no driver waits forever: after a configurable timeout it should give up and finish, so the simulation always terminates.
- [ ] Limit the number of parking attempts per driver and wait a little between them, so a full parking lot does not cause an endless retry loop.
- [ ] Make price negotiation move in one direction only: each new driver offer must be at least the previous one, and each new manager counter-offer must be at most the previous one, never going below the manager's minimum or outside the driver's budget. Today the driver can offer less after the manager has already lowered the price.
- [ ] Add a second (and maybe a third) parking environment with different prices.
- [ ] Measure again after the queue is in place: today, with 50 drivers and 10 spots, a run takes about 40-52s and many drivers still fail once before getting a spot.
