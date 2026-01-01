# Vacuum Chamber Specifications

The ecoAtom vacuum chamber is a simplified dynamic pressure model.

## Parameters

- Initial pressure (Pa)
- Base pressure (Pa) — theoretical minimum
- Pump speed — how aggressively the system approaches base pressure
- Outgassing rate — tendency of surfaces/leaks to increase pressure

The pressure evolves over time using:

- A pumping term that pulls towards the base pressure.
- An outgassing term that pushes pressure upward, especially at higher pressure.

This yields a realistic-looking pump-down curve that can be tuned via config.