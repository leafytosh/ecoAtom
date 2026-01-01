# Centrifugal Core Design

The centrifugal core in ecoAtom is a simplified rotational accelerator.

## Parameters

- Radius (m)
- RPM (rotations per minute)
- Angular velocity (rad/s)
- Tangential velocity (m/s)
- Centrifugal acceleration (m/s²)
- Beam mass number (A)
- Instability threshold RPM

The core ramps up RPM over time:
- Below the instability threshold, the beam is considered "stable".
- Above the threshold, the system is more likely to generate energetic, fragment-rich events.

The current implementation uses a non-relativistic kinetic energy approximation to produce
consistent scaling for event generation. It is deliberately simplified so the code remains
readable and modifiable.