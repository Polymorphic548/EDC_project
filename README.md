# Diode-Compensated Current Mirror PCB

A single-sided PCB containing two independent, diode-compensated 2N3904 current mirrors. This repository includes the original LTspice circuit, KiCad schematic and layout, assembly drawings, and matched Gerber and drill files.

Each circuit has a power connector and three voltage-measurement headers: across the load and across each transistor's base and emitter.

| Specification | Design |
|---|---|
| Panel size / thickness | 150 x 100 mm / 1.7 mm |
| Circuits | Two electrically isolated copies, A and B |
| Copper | Single-sided, B.Cu |
| Track width / configured minimum clearance | 0.6 mm / 0.8 mm |
| Supply | 9.8 V DC per circuit |
| Assembly | Through-hole; 36 footprints including eight 2-pin headers |
| Header pitch | 2.54 mm |
| Adjustment resistor | Fixed 120 ohm; no trimmer |
| Software | KiCad 10.0.7 or later |

The saved design and exports pass the recorded CAD and geometry checks. **The rectangular-pad export still requires confirmation in the lab's CopperCAM installation.** Physical circuit performance has not been measured.

## Open the design

1. Open [dual_current_mirror.kicad_pro](PCB%20layout/dual_current_mirror.kicad_pro) in KiCad.
2. Open [dual_current_mirror.kicad_pcb](PCB%20layout/dual_current_mirror.kicad_pcb) in PCB Editor.
3. Press **Alt+3** for the 3D Viewer.

The [single-circuit project](PCB%20layout/current_mirror.kicad_pro) is a reusable 78 x 67 mm unit. Use the **dual** project for the complete panel.

![Current panel assembly drawing](PCB%20layout/previews/dual_panel_assembly.png)

[Copper preview](PCB%20layout/previews/dual_panel_copper_review.png) | [Panel schematic PDF](PCB%20layout/previews/dual_panel_schematic.pdf)

The supplied KiCad screenshot below shows the current placement and routing before the rectangular-pad update. The generated drawing above shows the current pads.

![KiCad view of the two isolated circuits](PCB%20layout/Screenshot%202026-10-31%20121807.png)

## Circuit and components

The input passes through a 1 ohm resistor and a series 1N4007 diode. A Zener and two signal diodes provide the compensation network. Each transistor has a 22 ohm emitter resistor, and the output drives a 1 kohm load. The LTspice parameterized resistor RV1 is implemented as fixed R7/R107, nominally 120 ohm.

![Original LTspice schematic](schematics/Screenshot%202026-10-31%20084318.png)

| Copy A | Copy B | Component / value |
|---|---|---|
| R1 | R101 | 1 ohm, 1/4 W input resistor |
| R2 | R102 | 662 ohm, 1/4 W |
| R3 | R103 | 1 kohm, 1/4 W |
| R4, R5 | R104, R105 | 22 ohm, 1/4 W emitter resistors |
| R6 | R106 | 1 kohm, 1/4 W load |
| R7 | R107 | Fixed 120 ohm, 1/4 W |
| D1, D2 | D101, D102 | 1N4148 |
| D3 | D103 | BZX55C5V1, 5.1 V Zener |
| D4 | D104 | 1N4007 |
| Q1, Q2 | Q101, Q102 | 2N3904 |
| C1 | C101 | 1.33 nF, at least 25 V |
| J1-J4 | J101-J104 | Four 1x2 male headers, 2.54 mm pitch |

See the [panel BOM](PCB%20layout/panel_BOM.csv) for the complete assembly list. Two populated circuits require two sets of parts and eight headers total. R1 is a resistor, not a fuse.

The original nominal 120 ohm resistor measured 117.6 ohm; measure the second circuit's resistor separately. The supplied LTspice results report approximately **4.625 mA at 25 degrees C** and **4.667 mA at 75 degrees C** with RV=117.6 ohm. These are source simulation results, not PCB measurements.

## Power and measurements

| Connection | Copy A | Copy B | Pin 1: positive / red | Pin 2: negative / black |
|---|---|---|---|---|
| Power input | J1 | J101 | VIN, +9.8 V | GND |
| Load voltage | J2 | J102 | VCC | OUT |
| First transistor VBE | J3 | J103 | BASE | E1 |
| Second transistor VBE | J4 | J104 | BASE | E2 |

Use **DC voltage mode**, with meter leads in COM and V/ohm. The circuit operates normally without a meter. These connectors must not be fitted with shorting caps.

VCC is the internal supply after the input resistor and diode. E1 and E2 are separate emitter nodes above their 22 ohm resistors; neither is ground. Copy B's transistors are Q101 and Q102.

Calculate output current using `Iout = Vload / Rload`. With a 1 kohm load, 5.00 V corresponds to 5.00 mA.

The circuits share no PCB nets, including ground. A common external supply or common-ground instrument can connect them externally.

## Fabrication

Use [dual_panel_machine_files.zip](PCB%20layout/fabrication/dual_panel_machine_files.zip) for the lab handoff. The [rectangle-pad package](PCB%20layout/fabrication/dual_panel_coppercam_rectangles.zip) contains identical files under a distinct name for a fresh CopperCAM import.

| File inside the package | Purpose |
|---|---|
| `dual_current_mirror-B_Cu.gbr` | Copper to retain; the only copper layer |
| `dual_current_mirror.drl` | Excellon drill locations and sizes |
| `dual_current_mirror-Edge_Cuts.gbr` | Optional outer 150 x 100 mm outline |
| `dual_current_mirror-Centre_Cut.gbr` | Optional straight centre separation line |

The package also contains a drill map, tool report, setup data, verification results and checksums. All geometry uses millimetres and a shared absolute origin. Apply fixture mirroring or positioning consistently to all layers. Through-hole pads may appear on F.Cu in KiCad, but only the **bottom copper pattern** is fabricated.

Extract into a fresh folder and open the copper Gerber in a new CopperCAM circuit. Before calculating contours, confirm that all three rectangular pads on each of the four transistors are visible. Import the drill file and verify that every hole aligns with its pad; the lab previously achieved registration using layers 1 and 5. Inspect the calculated isolation paths before machining. The copper export uses only standard circle and rectangle pad apertures.

### Centre separation

The optional centreline runs at **x=75 mm** across the panel. A centred 0.8 mm cutter leaves nominal **74.6 x 100 mm** halves without outer trimming.

[Centre-cut setup data](PCB%20layout/centre_cut_setup.json) records a **Roland monoFab SRM-20**, 1.7 mm board, 0.8 mm cutting diameter and maximum 0.4 mm depth per pass. **No executable cutting program is included.** The operator must confirm feeds, spindle speed, safe Z, zero reference, cutter suitability, breakthrough allowance, work holding and output format. Secure both halves and complete isolation and drilling before separation.

### Printed masks

[Unmirrored copper PDF](PCB%20layout/fabrication/dual_panel_BCu_unmirrored_1to1.pdf) | [Mirrored copper PDF](PCB%20layout/fabrication/dual_panel_BCu_mirrored_1to1.pdf)

For transfer or photoresist fabrication, confirm orientation and exposure polarity with the lab. Print at **100% / Actual Size** and measure the **50 mm calibration line**. Black denotes copper to retain. Transfer only the board area; calibration marks sit outside it. Assembly and review drawings are not fabrication masks.

## Assembly

Fit components on the face opposite the copper and solder on the copper side. There is no solder mask; use controlled amounts of flux-cored solder and inspect nearby joints for bridges.

- Verify the actual transistor manufacturer's pinout. CAD numbering is **1=emitter, 2=base, 3=collector**.
- All transistor and header pads are rectangular: **pad shape does not identify pin 1**. Follow numbering and assembly labels.
- Confirm physical fit: resistor pitch 7.62 mm, capacitor pitch 5 mm, transistor and header pitch 2.54 mm.
- Header holes are 1.0 mm; transistor holes are 0.8 mm. The panel also has 1.1 mm diode holes.
- Check diode polarity and power-connector orientation before applying power.

## Repository guide

| Location | Contents |
|---|---|
| [schematics/](schematics/) | Original LTspice schematic and related source files |
| [PCB layout/](PCB%20layout/README.md) | KiCad projects, BOMs and technical documentation |
| [Project.pretty/](PCB%20layout/Project.pretty/) | Shared project-local footprints |
| [previews/](PCB%20layout/previews/) | Assembly, schematic and copper review drawings |
| [fabrication/](PCB%20layout/fabrication/) | Machine packages and 1:1 masks |
| [reports/](PCB%20layout/reports/) | CAD checks, geometry audits and revision records |
| [scripts/](PCB%20layout/scripts/) | Design generation, export and verification utilities |

Recorded checks report zero ERC/DRC violations, zero unconnected items and zero schematic-parity issues for both projects under their configured rules. Independent audits verify isolated A/B nets, header connections, pad-to-netlist agreement and matching export geometry: **76 pads, 76 holes and 100 panel track segments**.

[Panel audit](PCB%20layout/reports/panel_audit.json) | [Export verification](PCB%20layout/fabrication/machine_files/verification.json) | [Pad audit](PCB%20layout/reports/coppercam_pads.json)

These checks establish saved-file consistency. Lab import, toolpaths, machining and physical circuit performance require verification on the actual equipment. Earlier revision records remain in `reports/`.

## License

This project is licensed under the [MIT License](LICENSE).
