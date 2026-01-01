# ecoAtom/core/centrifugal_core.py

"""
Centrifugal core model.

Simplified rotational accelerator:
- Radius (m)
- RPM (rotations per minute)
- Angular velocity (rad/s)
- Tangential velocity (m/s)
- Centrifugal acceleration (m/s^2)
- Instability threshold (RPM)
"""

from dataclasses import dataclass
import math
from typing import Dict


@dataclass
class CentrifugalState:
    rpm: float
    angular_velocity: float
    tangential_velocity: float
    centrifugal_acceleration: float
    unstable: bool


class CentrifugalCore:
    def __init__(self, cfg: Dict[str, float]) -> None:
        self.radius_m = cfg["radius_m"]
        self.rpm = cfg["initial_rpm"]
        self.max_rpm = cfg["max_rpm"]
        self.acceleration_rpm_per_s = cfg["acceleration_rpm_per_s"]
        self.beam_mass_number = cfg["beam_mass_number"]
        self.instability_threshold_rpm = cfg["instability_threshold_rpm"]

    @property
    def angular_velocity(self) -> float:
        return (self.rpm / 60.0) * 2.0 * math.pi  # rad/s

    @property
    def tangential_velocity(self) -> float:
        return self.angular_velocity * self.radius_m  # m/s

    @property
    def centrifugal_acceleration(self) -> float:
        return self.angular_velocity**2 * self.radius_m  # m/s^2

    @property
    def unstable(self) -> bool:
        return self.rpm >= self.instability_threshold_rpm

    @property
    def kinetic_energy_per_nucleon_j(self) -> float:
        """
        Non-relativistic KE per nucleon (J). We only need consistent scaling.
        KE = 1/2 m v^2 with m = nucleon mass ≈ 1.67e-27 kg.
        """
        v = self.tangential_velocity
        m = 1.67e-27
        return 0.5 * m * v * v

    def step(self, dt: float) -> CentrifugalState:
        """
        Advance RPM over time by a fixed ramp rate until saturated at max_rpm.
        """
        if self.rpm < self.max_rpm:
            self.rpm += self.acceleration_rpm_per_s * dt
            if self.rpm > self.max_rpm:
                self.rpm = self.max_rpm

        return CentrifugalState(
            rpm=self.rpm,
            angular_velocity=self.angular_velocity,
            tangential_velocity=self.tangential_velocity,
            centrifugal_acceleration=self.centrifugal_acceleration,
            unstable=self.unstable,
        )
