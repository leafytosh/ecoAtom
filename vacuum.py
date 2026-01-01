# ecoAtom/core/vacuum.py

"""
Vacuum chamber model.

Parameters:
- initial_pressure_pa
- base_pressure_pa
- pump_speed
- outgassing_rate

Simplified dynamic:
  dP/dt = -pump_speed * (P - base_pressure) + outgassing_rate * f(P)
"""

from dataclasses import dataclass
import math
from typing import Dict


@dataclass
class VacuumState:
    pressure_pa: float


class VacuumChamber:
    def __init__(self, cfg: Dict[str, float]) -> None:
        self.pressure_pa = cfg["initial_pressure_pa"]
        self.base_pressure_pa = cfg["base_pressure_pa"]
        self.pump_speed = cfg["pump_speed"]
        self.outgassing_rate = cfg["outgassing_rate"]

    def step(self, dt: float) -> VacuumState:
        # Pumping term: exponential-like approach to base pressure
        pump_term = -self.pump_speed * (self.pressure_pa - self.base_pressure_pa)

        # Outgassing term: weak upward pressure, more active at higher P
        outgas_term = self.outgassing_rate * math.log10(
            max(self.pressure_pa, 1e-12) * 1e12 + 10.0
        )

        dP = (pump_term + outgas_term) * dt
        self.pressure_pa += dP

        # Bound pressure
        if self.pressure_pa < self.base_pressure_pa:
            self.pressure_pa = self.base_pressure_pa
        if self.pressure_pa < 1e-12:
            self.pressure_pa = 1e-12

        return VacuumState(pressure_pa=self.pressure_pa)
