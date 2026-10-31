# P5: hand-soldering clearance, 2026-10-31

The user requested wider spacing around the marked header, transistor, nearby emitter-resistor and diode joints in both isolated copies before milling.

## P5 hand-soldering clearance update ? 2026-10-31

Both copies now use **0.8 mm minimum copper clearance**, with **0.6 mm tracks**. Header and transistor pin pitch remains **2.54 mm**. Their elongated pads are **1.7 mm along the pin row and 2.4 mm across it**, increasing the adjacent-pad gap from **0.54 to 0.84 mm**, while retaining soldering area. Header drills remain 1.0 mm; transistor drills remain 0.8 mm. Minimum copper around the holes is 0.35 mm for headers and 0.45 mm for transistors.

D1/D2 and D101/D102 were repositioned to spread the closely grouped diode joints. The two neighbouring diode-pad gaps are now **1.56 mm and 2.18 mm**. Those diode pairs are intentionally connected by the circuit; the 0.8 mm rule protects copper on different nets. Transistor outline graphics are on the assembly layer so they do not overlap the elongated lands.

The complete panel remains **150 x 100 mm**, with two isolated circuits. Electrical values, header functions, transistor pin numbering and hole diameters are preserved. There is no solder mask: use small amounts of solder and inspect for bridges. Use the regenerated **P5 ZIP**, not an earlier downloaded package. See `reports/solder_clearance.json` and `reports/P5_solder_clearance_2026-10-31/README.md`.

## Validation

Native KiCad ERC and DRC, including schematic parity, are rerun for both projects with the 0.8 mm copper clearance enforced. `../solder_clearance.json` checks both copies' pad dimensions, 2.54 mm pitch, retained drills, annular copper and diode spacing. The existing unit/panel audits verify values, all pad nets, isolation, panel fit and unique identifiers. The machine-file checker independently compares the new Gerber pad/track geometry and drill centres/sizes with the saved panel. No simulation or hardware test is implied.

The local pre-edit snapshot is in the ignored `current_mirror-backups/before_P5_solder_clearance_2026-10-31/` folder. P4 reports are historical. Open `dual_current_mirror.kicad_pcb` for the revised panel, and reload from disk if an older layout is open in KiCad.
