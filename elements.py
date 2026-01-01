# ecoAtom/core/elements.py

"""
Periodic table loading utilities.

Expected JSON format:
{
  "elements": [ { ... }, { ... }, ... ]

"""

from pathlib import Path
import json
from typing import List, Dict, Any


def load_elements(path: Path) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["elements"]
