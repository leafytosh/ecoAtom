# ecoAtom/modules/vacuum_chamber.py

"""
Wrapper around core.vacuum.VacuumChamber for higher-level composition.
"""

from typing import Dict, Any
from core.vacuum import VacuumChamber


def create_vacuum_chamber(config: Dict[str, Any]) -> VacuumChamber:
    return VacuumChamber(config["vacuum"])
