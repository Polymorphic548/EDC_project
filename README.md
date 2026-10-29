# EDC project: 5 mA analog current mirror PCB

This repository contains the group's LTspice circuit and its KiCad translation into a **single-sided, through-hole PCB** for college chemical etching. The design uses a 12 V DC supply and targets approximately 5 mA through an on-board 1 kohm load.

**Current revision: P1, provisional. Do not fabricate yet.** The user-measured trimmer hole pattern is fitted: **9 mm body, 8 mm across the opposite pair, third pin 5 mm from the centre**. Its actual wiper and physical pad roles remain unverified. Fabrication is targeted for **Friday, 30 October 2026**, after the remaining checks below.

## Open and view the board

Use **KiCad 10.0.7 or later**.

1. Open [the KiCad project](PCB%20layout/current_mirror.kicad_pro).
2. Double-click `current_mirror.kicad_pcb` in the project tree to open the PCB Editor.
3. Press **Alt+3**, or choose **View > 3D Viewer**, to see the assembled board.

You can also open [the PCB file](PCB%20layout/current_mirror.kicad_pcb) directly in the PCB Editor. Windows may hide its extension; choose the file with type **KiCad Board**, rather than KiCad Project or KiCad Schematic. No separate 3D file needs to be opened.

All 14 referenced standard-component 3D models were verified as installed on the development laptop. RV1 has a measured 2D footprint but no body model because its height/model is unconfirmed; the measurement points appear as pads rather than modeled pins.

For a quick view without KiCad:

- [Top assembly preview](PCB%20layout/previews/assembly_top.png)
- [Bottom copper review](PCB%20layout/previews/copper_review.png)
- [Schematic preview](PCB%20layout/previews/schematic.png)

These are **draft review images**, not production printing masks.

## Files and folders

| Location | Contents |
|---|---|
| [schematics/](schematics/) | Original LTspice `.asc`, saved `.log`, `.raw` simulation data and `.db` database |
| [PCB layout/](PCB%20layout/) | Editable KiCad project, schematic and board |
| [PCB layout/README.md](PCB%20layout/README.md) | Detailed electrical mapping, physical assumptions, fabrication and regeneration instructions |
| [BOM.csv](PCB%20layout/BOM.csv) | Component list and footprint status |
| [components.json](PCB%20layout/components.json) | Component values, connections, footprint basis and placement |
| [Project.pretty/](PCB%20layout/Project.pretty/) | Project-local footprints, including enlarged etching pads and the RV1 placeholder |
| [previews/](PCB%20layout/previews/) | Schematic, assembly and copper review PDFs/PNGs |
| [reports/](PCB%20layout/reports/) | Connectivity checks, ERC/DRC reports, design hashes and trimmer review |
| [Baseline re-review](PCB%20layout/reports/review_2026-10-28/README.md) | Historical P0 review on 28 October 2026 |
| [P1 update](PCB%20layout/reports/update_2026-10-29/README.md) | Measured trimmer geometry, pending pinout and updated validation |
| [scripts/](PCB%20layout/scripts/) | Project generation, routing, checking and preview export helpers |
| [fabrication/](PCB%20layout/fabrication/) | Release-status notice; no production copper mask is released at P1 |

## Circuit and components

The source of truth for the circuit connections is [the original LTspice schematic](schematics/diode_comp_mirror_enhanced_v2.asc). The KiCad translation retains that circuit, adds a two-point external supply connection and six measurement pads, and implements the adjustable resistor using a three-pin trimmer with its wiper tied to one end. No extra fuse was added.

| KiCad reference | LTspice reference | Component |
|---|---|---|
| J1 | V1 | External 12 V supply connection replaces the ideal simulated source |
| R1 | F1 | 1 ohm resistor, 1/4 W; **not a fuse** |
| D4 | D4 | 1N4007 series input diode |
| R2 | Rs | 620 ohm resistor, 1/4 W |
| D3 | Dz | 5.1 V Zener, intended physical part BZX55C5V1 |
| D1, D2 | D1, D2 | Two 1N4148 diodes |
| R3 | R1a | 1 kohm resistor, 1/4 W |
| RV1 | RV1 | Intended 500 ohm adjustable resistor; simulated setting approximately 119.8 ohm |
| Q1, Q2 | Q1, Q2 | Two 2N3904 transistors |
| R4, R5 | Re1, Re2 | Two 22 ohm resistors, 1/4 W |
| R6 | Rload | 1 kohm load resistor, 1/4 W |
| C1 | C1 | 100 nF capacitor, rated at least 25 V |

The listed resistor values are available in the group's inventory; no additional series/parallel resistor network is currently required. The approximately 119.8 ohm value is a **trimmer setting**, not a separate fixed resistor to purchase. Actual adjustment may differ because of component tolerances.

Power flows from **J1 pin 1 / VIN**, through R1 and D4, to **VCC**. **J1 pin 2 is GND**. The series diode provides reverse-polarity blocking; it does not provide general short-circuit protection.

## Measurement pads and normal operation

`TP` means **test point**. Each pad is connected to an existing circuit node. The copper ring remains connected to the bottom track despite the hole in its centre. You can touch a probe to the ring or solder in a suitable test pin/wire. **The circuit operates normally with no multimeter connected.**

| Pad | Connected node | Purpose |
|---|---|---|
| TP1 | GND | Common voltage reference |
| TP2 | VIN | Incoming supply, before R1 and D4 |
| TP3 | VCC / LOAD+ | Supply after R1 and D4; upper end of R6 |
| TP4 | VA | Reference node joining R2, the Zener cathode and R3 |
| TP5 | BASE | Both transistor bases and Q1's collector |
| TP6 | OUT / LOAD- | Q2's collector and lower end of R6 |

Connect the supply to **J1**, positive to VIN and negative to GND. Test points are measurement access points, not additional required supply connections.

To estimate output current:

1. Set the multimeter to **DC volts**.
2. Put the red probe on **TP3** and the black probe on **TP6**.
3. Calculate `Iout = (V(TP3) - V(TP6)) / R6`.

With nominal R6 = 1000 ohm, **5.00 V corresponds to 5.00 mA**. Resistor tolerance affects the estimate. Do not connect a meter in current mode across TP3 and TP6: that bypasses the load. The board has no separate series current-measurement break.

## Layout and current validation

- Board outline: **78 x 67 mm**.
- Through-hole components on top; all routed tracks on **B.Cu**, the bottom copper layer.
- Track width: **0.6 mm**; configured minimum copper clearance: **0.4 mm**.
- No vias, wire jumpers or copper pours.
- The KiCad file uses its normal two-copper-layer data model for through-hole pads; the fabrication pattern uses **bottom copper only**.
- RV1 has an **18 x 14 mm** reserved area, clear of other component bodies/pads.

The current P1 checks, run on **29 October 2026 with KiCad 10.0.7**, report:

| Validation | Result |
|---|---|
| Original LTspice connectivity vs translated circuit | All 12 circuit nets match |
| Fresh schematic ERC | 0 reported errors or warnings |
| Fresh PCB DRC | 0 reported errors or warnings |
| Unconnected items | 0 |
| Schematic-to-PCB parity issues | 0 |
| Native exported schematic netlist vs board pads | Exact match |
| Component values and six test-point connections | Checked |
| Bottom-layer routing and RV1 reserved area | Checked |

The JSON reports record the active severities and standard ignored check categories. These results establish consistency of the provisional CAD files, **not physical component fit, fabricated-board performance or temperature stability**. No physical board has been assembled or measured. Source/design SHA-256 hashes are saved in [design_sha256.json](PCB%20layout/reports/design_sha256.json).

## What still needs confirmation

1. **RV1:** identify the physical wiper and confirm the intended **500 ohm** resistance. The custom footprint now uses the user's **9 mm body, 8 mm opposite-pair spacing and 5 mm third-pin offset**; it does not substitute an inferred RM065 footprint. **Offset pad 2 is only a provisional wiper assignment.** The 1 mm drill diameter remains an assumption to check against the real leads. The original inventory's multiturn description is not confirmed. See the [P1 update](PCB%20layout/reports/update_2026-10-29/README.md); the [older photo review](PCB%20layout/reports/trimmer_photo_review.md) records the earlier tentative identification.
2. **Transistors:** verify the actual manufacturer's pinout against the assumed **1 = emitter, 2 = base, 3 = collector** footprint. The chosen wide footprint requires lead forming to 2.54 mm pitch.
3. **Capacitor:** confirm C1's assumed **5 mm lead spacing**.
4. **Connections:** J1 uses 2.54 mm-spaced holes for a header or soldered wires; it is not a 5.08 mm screw-terminal footprint. Supply hardware and optional test pins are additional to the listed electronic components.
5. **College process:** confirm achievable clearances, mask polarity, required mirroring, transfer method and printing scale.

Once RV1's wiper is identified, confirm or correct the physical pad-to-net mapping in **both schematic and PCB**, preserve the wiper-to-end connection, rerun checks and update release status. The original P0 2.54 mm-spaced placeholder has been replaced. For a fit check, use the [1:1 trimmer fitting template](PCB%20layout/previews/trimmer_fit_check.pdf); print at actual size and verify its calibration line. It is not a copper mask.

## Fabrication handoff

After the physical checks and final layout update:

1. Rerun ERC and PCB DRC with schematic parity; verify bottom-only routing.
2. Export a **B.Cu-only copper mask at 1:1 scale**, with drill-centre marks if requested by the college.
3. Keep the outline and assembly drawing separate from the copper pattern.
4. Confirm whether the college needs mirrored or unmirrored artwork and positive or negative mask polarity. The process is not yet confirmed as toner transfer versus photoresist.
5. Disable printer fit-to-page/scaling and verify printed dimensions using the known board outline or a calibration mark.

The current copper review PDF includes an outline and draft notices. **Do not use it as a production mask.** Gerber/drill files can be prepared if the college accepts them.

## Temperature experiment

The saved LTspice log reports approximately **4.99945 mA at 25 C** and **5.00011 mA at 75 C**. Those are the friend's existing simulation results; the PCB translation has not been physically temperature-tested and no new SPICE simulation was run.

For a physical experiment, first adjust near 5 mA at a measured room temperature, then leave RV1 unchanged. Use a temperature probe and controlled lab heating to warm the circuit evenly, wait for stable readings, and record temperature alongside the voltage between TP3 and TP6. The simulation varies circuit temperature uniformly; heating only one transistor is a different test. Test only within the confirmed ratings of **every actual component**, including the pending trimmer. Without controlled equipment, report a qualitative trend and the temperatures actually reached rather than claiming a verified 25-75 C sweep.

## Working on the files

Edit the saved project in KiCad for normal design work. The [PCB README](PCB%20layout/README.md#reproduce-the-provisional-files) contains the generation, checking and preview commands for the installed Windows tools.

**The generator recreates provisional P1 and can overwrite manual layout changes.** Its trimmer geometry matches the user measurements, but its pad roles remain provisional until the wiper test. Preserve manual edits and update the definitions before using it after final pinout confirmation. Project-local footprints should travel with the KiCad files. Optional PNG rendering uses the laptop's existing Python/PyMuPDF installation; KiCad produces the PDFs.

An early KiCad Python/SWIG track-removal operation caused an access violation. The saved routing helper avoids that operation, and the corrected route and subsequent checks completed successfully. Opening the board or its 3D viewer does not require a Python process to stay running.
