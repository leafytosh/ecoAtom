# ecoAtom

ecoAtom is a **centrifugal atom collider and vacuum chamber simulator**.

It treats the project like a digital research facility:

- A centrifugal core that spins a beam of atoms.
- A dynamic vacuum chamber model.
- Synthetic collision event generation.
- A modular beamline and detector concept.
- A browser-based "control room" UI.

The physics are simplified but **internally consistent**, designed to feel plausible and to generate
structured data you can analyze, visualize, or build stories around.

---

## Project structure

```text
ecoAtom/
??? core/
?   ??? simulate.py           # main simulation loop
?   ??? centrifugal_core.py   # rotational accelerator model
?   ??? vacuum.py             # vacuum chamber dynamics
?   ??? elements.py           # periodic table loader
?   ??? events.py             # collision event generator + writer
??? data/
?   ??? periodic_table.json   # element properties (partial; extendable)
?   ??? config.json           # simulation + machine configuration
?   ??? events/               # generated event JSON files
??? ui/
?   ??? index.html            # control room mock UI
?   ??? main.js               # front-end demo logic
?   ??? style.css             # decorative styling
?   ??? animations.css        # CSS animations
??? modules/
?   ??? vacuum_chamber.py     # wrapper for vacuum subsystem
?   ??? detector.py           # conceptual detector model
?   ??? beamline.py           # ties core + vacuum + detector
??? docs/
?   ??? facility_overview.md
?   ??? centrifugal_design.md
?   ??? vacuum_chamber_specs.md
??? main.py                   # facility startup entry point
??? requirements.txt