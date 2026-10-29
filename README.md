# EDC project: 5 mA analog current mirror PCB

This repository contains the original LTspice circuit and its KiCad translation into a **single-sided, through-hole PCB** for college chemical etching. The circuit uses a 12 V supply and an on-board 1 kohm output load.

**Current revision: P2 - fixed 120 ohm resistor.** At the user's request, the trimmer is removed and replaced with **R7, one nominal 120 ohm resistor**, between TRIM_TOP and BASE. The user's physical resistor measured **117.6 ohm**. There is no trimmer or wiper assignment in the current circuit. Physical-part fit and the college's printing requirements still need checking before fabrication, targeted for Friday, 30 October 2026.

## Open and view

1. Open [the KiCad project](PCB%20layout/current_mirror.kicad_pro) with KiCad 10.0.7 or later.
2. Open [current_mirror.kicad_pcb](PCB%20layout/current_mirror.kicad_pcb) in the PCB Editor. In Windows, choose the file whose type is **KiCad Board**.
3. Press **Alt+3**, or choose **View > 3D Viewer**. R7 uses the same axial resistor body/footprint family as the other quarter-watt resistors.

Quick reviews: [assembly preview](PCB%20layout/previews/assembly_top.png), [copper review](PCB%20layout/previews/copper_review.png), and [schematic preview](PCB%20layout/previews/schematic.png). These are review drawings, not production masks. Reopen the board from disk after an external update; an already-open editor may show its old in-memory copy.

## Repository contents

| Location | Contents |
|---|---|
| [schematics/](schematics/) | Original LTspice ASC, saved log, raw simulation data and database |
| [PCB layout/](PCB%20layout/) | Editable KiCad project, schematic and PCB |
| [PCB README](PCB%20layout/README.md) | Component mapping, fabrication assumptions and reproduction commands |
| [BOM](PCB%20layout/BOM.csv) / [component data](PCB%20layout/components.json) | Parts, footprints, nets and R7's reported measured value |
| [Project.pretty](PCB%20layout/Project.pretty/) | Local etching-oriented footprints, including R7_ETCH |
| [P2 change record](PCB%20layout/reports/P2_fixed120_2026-10-29/README.md) | Fixed-resistor substitution and validation |
| [reports/](PCB%20layout/reports/) | Current ERC/DRC, source connectivity, routing and hashes; historical P0/P1 reviews |
| [scripts/](PCB%20layout/scripts/) | Regeneration, routing, checking and preview export helpers |
| [fabrication/](PCB%20layout/fabrication/) | Release status; no production copper mask is released |

The P1 trimmer fit template, measured footprint and reports are retained only as historical records. They do not apply to P2. The original LTspice files are preserved, including their 119.8 ohm RV1 setting; the current KiCad circuit intentionally differs at R7.

## Components and power

| KiCad | LTspice | Component |
|---|---|---|
| J1 | V1 | External 12 V connection |
| R1 | F1 | 1 ohm, 1/4 W resistor; not a fuse |
| D4 | D4 | 1N4007 series input diode |
| R2 | Rs | 620 ohm, 1/4 W |
| D3 | Dz | 5.1 V Zener, intended part BZX55C5V1 |
| D1, D2 | D1, D2 | 1N4148 |
| R3 | R1a | 1 kohm, 1/4 W |
| R7 | Replaces RV1 | **120 ohm, 1/4 W fixed resistor**; supplied part measured 117.6 ohm |
| Q1, Q2 | Q1, Q2 | 2N3904 |
| R4, R5 | Re1, Re2 | 22 ohm, 1/4 W, between each emitter and ground |
| R6 | Rload | 1 kohm, 1/4 W output load |
| C1 | C1 | 100 nF, rated at least 25 V |

Connect supply positive to **J1 pin 1 / VIN** and negative to **J1 pin 2 / GND**. The input path is VIN -> R1 -> D4 -> VCC. D4 provides reverse-polarity blocking; no fuse or general short-circuit protection was added. R7 is not adjustable. Its resistance tolerance and other real-part differences may change the output current from the original simulation.

The CAD pin mapping for Q1/Q2 is **1=emitter, 2=base, 3=collector**. The 22 ohm resistors connect to the emitters. Verify the actual manufacturer's package pinout before soldering; the wide footprint requires lead forming to 2.54 mm spacing. The D-shaped outline is the package body, not a circuit-symbol arrow.

## Test pads and multimeter

Test pads remain electrically connected when no meter is present; the circuit works without probes. Touch the copper ring or solder in a suitable test pin/wire.

| Pad | Node | Use |
|---|---|---|
| TP1 | GND | Common voltage reference |
| TP2 | VIN | Incoming supply before R1/D4 |
| TP3 | VCC / LOAD+ | Supply after R1/D4; top of R6 |
| TP4 | VA | Reference node joining R2, Zener cathode and R3 |
| TP5 | BASE | Shared transistor bases and Q1 collector |
| TP6 | OUT / LOAD- | Q2 collector and bottom of R6 |

For output-current inference, use **DC voltage mode**, red probe TP3 and black probe TP6. `Iout = (V(TP3) - V(TP6)) / R6`. With nominal R6=1000 ohm, **5.00 V means 5.00 mA**. Use COM and V/ohm sockets. Do not connect current mode across these pads: it bypasses the load. There is no series current-measurement break. With fixed R7, there is no current-adjustment screw.

## Board and validation

- Outline **78 x 67 mm**; through-hole components on top.
- All tracks on **B.Cu**, minimum width **0.6 mm**, configured clearance **0.4 mm**.
- No vias, jumpers or copper pours. Through-hole pads use KiCad's normal two-layer data model; fabricate bottom copper only.
- R7 uses a 7.62 mm-spaced axial footprint with enlarged 2.2 mm pads and 0.8 mm drills.

The current P2 ERC/DRC and netlist audit reports record CAD results; see [the P2 change record](PCB%20layout/reports/P2_fixed120_2026-10-29/README.md). Source comparison preserves all 12 circuit nets while explicitly accounting for replacing LTspice RV1=119.8 ohm with fixed R7=120 ohm. [Design hashes](PCB%20layout/reports/design_sha256.json) identify the saved files. Reports list standard ignored check categories; no new exclusions were added for this revision.

No new SPICE simulation, physical PCB measurement or temperature validation has been performed for R7. The source log's approximately 4.99945 mA at 25 C and 5.00011 mA at 75 C apply to the **original simulated 119.8 ohm setting**, not the new 120 ohm nominal / 117.6 ohm measured part. For a physical temperature experiment, keep supply and circuit settings fixed, heat uniformly with a measured temperature, wait for stable readings, and record TP3-TP6 voltage. Stay within the verified ratings of every actual component.

## Before fabrication

1. Confirm actual transistor pinout, resistor body/lead fit and C1's assumed **5 mm lead spacing**.
2. J1 is a **2.54 mm header/solder-wire footprint**, not a 5.08 mm screw terminal. Optional supply/test-point hardware is additional to the electronic parts list.
3. Confirm the college's etching capability, mask polarity and mirrored/unmirrored transfer convention.
4. Rerun ERC/DRC with schematic parity after any design change.
5. Export **B.Cu only at 1:1**, keeping the outline/assembly drawing separate. Disable fit-to-page and verify actual print size using a calibration mark or the known outline.

The current copper review includes an outline and review notices. Do not use it as a production mask. A Gerber/drill set can be exported if the college accepts it.

## Working on the files

Use KiCad for normal editing. See [the PCB README](PCB%20layout/README.md#reproduce-p2) for regeneration commands. **The generator recreates P2 and can overwrite manual CAD edits**; preserve manual work and update definitions first. It preserves an existing project preference file. Local footprints must travel with the project.

The old P1 trimmer-update helper is retired and refuses to overwrite P2. An earlier KiCad Python track-removal crash is avoided by stripping serialized tracks before routing. Opening the saved board or 3D viewer does not require a Python process to remain running.
