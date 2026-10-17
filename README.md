# maspy-parking

Parking implementation using Maspy

## Run

```bash
make setup
make run
```

`make help` lists all available commands.

## Current version overview

Three actors communicate through the `Parking` channel:

- **Manager** – central agent. Receives spot requests and forwards a `park` goal
  to the requesting driver.
- **Driver** – asks the manager for a spot on startup and parks when it receives
  a `park` goal.
- **Parking** – the environment representing the parking lot (defined, but spot
  control is not implemented yet).

### Flow

1. On startup each `Driver` adds `Goal("ask_spot_available", <manager name>)`.
2. The driver sends `achieve Goal("find_spot_available")` to the manager over the
   `Parking` channel.
3. The manager's `search_empty_spot` plan adds `Goal("SendSpot", <driver>)`.
4. The manager's `send_spot_to_driver` plan sends `achieve Goal("park")` back.
5. The driver's `park_on_spot` plan runs and the driver stops its cycle.

The manager stops its cycle once no `Drv` agents are running.

### Limitations (next steps)

- The `Parking` environment is not used yet: no notion of occupied/available
  spots or capacity.
- Each driver requests a spot only once, at startup.
- No handling for more drivers than available spots.