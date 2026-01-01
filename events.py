# ecoAtom/core/events.py

"""
Collision event generation and persistence.

Events are generated from:
- centrifugal state (rpm, KE, instability)
- vacuum state (pressure)
- beam element properties (Z, mass)

Events are written as JSON to data/events/.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import json
import random


@dataclass
class Fragment:
    id: int
    energy_j: float
    angle_deg: float


@dataclass
class Event:
    timestamp: str
    step: int
    time_delta: float
    beam_element: Dict[str, Any]
    centrifugal_state: Dict[str, Any]
    vacuum_state: Dict[str, Any]
    fragments: List[Fragment]


def generate_event(
    step: int,
    dt: float,
    beam_element: Dict[str, Any],
    core_state: Dict[str, Any],
    vacuum_state: Dict[str, Any],
    base_ke_j_per_nucleon: float,
) -> Event:
    timestamp = datetime.utcnow().isoformat() + "Z"

    z = beam_element["atomic_number"]
    mass = beam_element["atomic_mass"]

    # Base total kinetic energy (scaled)
    total_energy_j = base_ke_j_per_nucleon * mass * 1e-9

    # Fragment count scales with Z, with randomness
    avg_fragments = max(2, min(10, int(z / 3)))
    n_fragments = random.randint(max(2, avg_fragments - 2), avg_fragments + 2)

    fragments: List[Fragment] = []
    remaining_energy = total_energy_j

    for i in range(n_fragments):
        if i == n_fragments - 1:
            e = max(0.0, remaining_energy)
        else:
            fraction = random.uniform(0.05, 0.3)
            e = total_energy_j * fraction
            remaining_energy -= e
        angle = random.uniform(0.0, 360.0)
        fragments.append(Fragment(id=i, energy_j=e, angle_deg=angle))

    return Event(
        timestamp=timestamp,
        step=step,
        time_delta=dt,
        beam_element={
            "atomic_number": beam_element["atomic_number"],
            "symbol": beam_element["symbol"],
            "name": beam_element["name"],
            "atomic_mass": beam_element["atomic_mass"],
        },
        centrifugal_state=core_state,
        vacuum_state=vacuum_state,
        fragments=fragments,
    )


def save_event(event: Event, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = event.timestamp.replace(":", "").replace("-", "").replace(".", "")
    filename = f"event_{event.step:06d}_{ts}.json"
    path = output_dir / filename

    serializable = asdict(event)
    serializable["fragments"] = [asdict(f) for f in event.fragments]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)

    return path
