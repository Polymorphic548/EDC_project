# P2: replace RV1 with a single fixed 120 ohm resistor

The user reported an apparently defective trimmer and explicitly requested a single fixed resistor instead. The replacement is **R7, nominal 120 ohm**, with a user-reported measured resistance of **117.6 ohm**. The CAD/BOM use the nominal value; `components.json` records the measurement.

## Electrical and physical change

- R7 pin 1 connects to **TRIM_TOP**, the junction with R3.
- R7 pin 2 connects to **BASE**, the common transistor base/Q1 collector node.
- The old RV1, its third pad and wiper/end tie are removed from the active schematic and PCB.
- R7 uses a project-local axial quarter-watt resistor footprint at **(45,38) mm**, with **7.62 mm lead spacing**, **2.2 mm copper pads** and **0.8 mm drills**. Confirm the physical resistor fits this assumed package.
- No particular resistor polarity is required. No series/parallel combination is used.
- Board outline remains **78 x 67 mm**. Other component positions and values are preserved. All tracks remain B.Cu, 0.6 mm, with no vias or jumpers.

The original LTspice schematic and saved simulation files are unchanged. Their RV1 value is 119.8 ohm; the fixed 120 ohm nominal / 117.6 ohm measured replacement is an intentional user-authorized value substitution. Source verification checks topology while explicitly recording this exception. No new SPICE simulation was run, and the original exact current/temperature results are not evidence for the modified physical circuit.

## Validation and handoff

Current reports are `../erc.json`, `../drc.json`, `../source_connectivity.json`, `../board_audit.json` and `../routing.json`. `checks.json` in this folder records the P2-specific geometry/value and preservation checks. `../design_sha256.json` identifies the current design files.

The standard physical/fabrication checks still apply: actual transistor manufacturer pinout, component lead fit, C1 pitch, and the college's mask polarity/mirror/printing process. The old trimmer identification issue no longer applies to P2. Historical P0/P1 footprints, templates and reports are retained for provenance only and are not active P2 components or fabrication assets.

Before regenerating P2, preserve any manual edits. A pre-P2 local snapshot is kept in the ignored `current_mirror-backups/before_P2_fixed120_2026-10-29/` folder. The P1 trimmer geometry updater is retired to prevent accidentally restoring the trimmer.
