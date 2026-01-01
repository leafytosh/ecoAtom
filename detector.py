# ecoAtom/modules/detector.py

"""
Conceptual detector model.

Right now this is not wired into the main loop, but it can be used
to post-process Event.fragments to simulate detection efficiency
and angular resolution.
"""

from typing import List, Dict, Any
import math
import random


class Detector:
    def __init__(self, cfg: Dict[str, Any]) -> None:
        self.efficiency = cfg.get("efficiency", 0.8)
        self.angular_resolution_deg = cfg.get("angular_resolution_deg", 5.0)

    def detect(self, fragments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        detected: List[Dict[str, Any]] = []

        for frag in fragments:
            if random.random() > self.efficiency:
                continue

            angle = frag["angle_deg"]
            binned_angle = self._bin_angle(angle)

            detected.append(
                {
                    "energy_j": frag["energy_j"],
                    "angle_deg": binned_angle,
                }
            )

        return detected

    def _bin_angle(self, angle_deg: float) -> float:
        step = self.angular_resolution_deg
        return round(angle_deg / step) * step
