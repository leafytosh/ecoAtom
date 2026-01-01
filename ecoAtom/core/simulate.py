# ecoAtom/core/simulate.py

"""
Main simulation loop for ecoAtom.

- Instantiates CentrifugalCore and VacuumChamber from config.
- Steps them in time.
- Periodically generates events using current state.
- Writes events to JSON under data/events/.
"""

from pathlib import Path
from typing import Dict, Any, List

from .centrifugal_core import CentrifugalCore
from .vacuum import VacuumChamber
from .events import generate_event, save_event


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def _select_beam_element(elements: List[Dict[str, Any]], atomic_number: int) -> Dict[str, Any]:
    for e in elements:
        if e["atomic_number"] == atomic_number:
            return e
    raise ValueError(f"No element with atomic_number={atomic_number} found.")


def run_simulation(elements: List[Dict[str, Any]], config: Dict[str, Any]) -> None:
    sim_cfg = config["simulation"]
    core_cfg = config["centrifugal"]
    vac_cfg = config["vacuum"]
    beam_cfg = config["beam"]
    output_cfg = config["output"]

    steps = sim_cfg["steps"]
    dt = sim_cfg["time_step"]
    event_interval = sim_cfg["event_interval_steps"]
    realtime_delay = sim_cfg.get("realtime_delay", 0.0)

    beam_element = _select_beam_element(elements, beam_cfg["element_atomic_number"])

    core = CentrifugalCore(core_cfg)
    vacuum = VacuumChamber(vac_cfg)

    events_dir = DATA_DIR / output_cfg["events_dir"]

    print(
        f"[INFO] Beam element: Z={beam_element['atomic_number']} "
        f"({beam_element['symbol']}) – {beam_element['name']}"
    )
    print(f"[INFO] Steps: {steps}, dt={dt}, event interval: {event_interval} steps")

    import time

    for step in range(steps):
        core_state = core.step(dt)
        vac_state = vacuum.step(dt)

        if step % event_interval == 0 and step != 0:
            event = generate_event(
                step=step,
                dt=dt,
                beam_element=beam_element,
                core_state={
                    "rpm": core_state.rpm,
                    "angular_velocity": core_state.angular_velocity,
                    "tangential_velocity": core_state.tangential_velocity,
                    "centrifugal_acceleration": core_state.centrifugal_acceleration,
                    "unstable": core_state.unstable,
                },
                vacuum_state={"pressure_pa": vac_state.pressure_pa},
                base_ke_j_per_nucleon=core.kinetic_energy_per_nucleon_j,
            )
            path = save_event(event, events_dir)
            print(
                f"[EVENT] step={step:04d} rpm={core_state.rpm:8.1f} "
                f"P={vac_state.pressure_pa:.3e} Pa "
                f"frags={len(event.fragments)} -> {path.name}"
            )

        if realtime_delay > 0:
            time.sleep(realtime_delay)

    print("[INFO] Simulation loop finished.")
