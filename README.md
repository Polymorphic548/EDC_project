# EDC project: two isolated current mirrors on one PCB

**Current revision: P4.** Two independent copies of the analog current-mirror circuit fit on a **150 x 100 mm (15 x 10 cm)** single-sided copper board. Each copy has male pin headers for power and exactly three voltage measurements: **Rload, Q1 base-emitter and Q2 base-emitter**. The earlier loose test pads are removed from the current designs.

## Open the two-copy panel

1. Open [dual_current_mirror.kicad_pro](PCB%20layout/dual_current_mirror.kicad_pro) in KiCad 10.0.7 or later.
2. Open [dual_current_mirror.kicad_pcb](PCB%20layout/dual_current_mirror.kicad_pcb) in the PCB Editor.
3. Press **Alt+3** for the 3D Viewer. The headers use standard vertical male-pin models.

[Panel assembly preview](PCB%20layout/previews/dual_panel_assembly.png) | [Panel copper review](PCB%20layout/previews/dual_panel_copper_review.png) | [Panel schematic PDF](PCB%20layout/previews/dual_panel_schematic.pdf)

The reusable **single-copy** project is still [current_mirror.kicad_pro](PCB%20layout/current_mirror.kicad_pro). Its board is 78 x 67 mm; it is not the full 15 x 10 cm panel. Reopen files from disk after external changes rather than saving an old in-memory layout over the new files.

## Layout and isolation

| Item | Dimensions / placement |
|---|---|
| Full copper blank / panel | 150 x 100 mm |
| Each unit, rotated 90 degrees | 67 x 78 mm |
| Copy A unit rectangle | x=5.5..72.5 mm, y=11..89 mm |
| Copy B unit rectangle | x=77.5..144.5 mm, y=11..89 mm |
| Gap between unit rectangles | 5 mm |
| Left/right margins | 5.5 mm |
| Top/bottom margins | 11 mm |

All tracks are on **B.Cu**: 0.6 mm width, 0.4 mm configured minimum clearance, no vias, copper pours or wire jumpers. Through-hole pads use KiCad's normal multi-layer data model; fabricate only the bottom copper pattern. The outer Edge.Cuts is 150 x 100 mm. The centre guide at x=75 mm is a drawing-layer cutting guide, not copper or a routed slot. The copies may remain on one piece of board while electrically separate.

Copy A uses the original references (Q1/Q2, R1..R7, J1..J4). Copy B uses references offset by 100 (Q101/Q102, R101..R107, J101..J104). All A_ and B_ nets are separate, **including both grounds**. A shared external supply, common-ground instrument or added wire can connect the two copies externally; the PCB itself provides no such connection.

## Header connections and multimeter use

Use **1x2 straight male headers, 2.54 mm pitch**, soldered from the copper side, and suitable female jumper-wire connectors. There are **four headers per copy, eight total / sixteen pins**. Each header has 1 mm drill holes and 2 mm copper pads. Copper pads/holes remain necessary for soldering the pins.

| Purpose | Copy A | Copy B | Pin 1 (square pad) | Pin 2 |
|---|---|---|---|---|
| Power input | J1 | J101 | +9.8 V / VIN | GND |
| Load voltage | J2 | J102 | VCC, top of load resistor | OUT, bottom of load / Q2-role collector |
| First transistor Vbe | J3 | J103 | BASE | First transistor emitter, above its 22 ohm resistor |
| Second transistor Vbe | J4 | J104 | BASE | Second transistor emitter, above its 22 ohm resistor |

For voltage measurements, use **DC volts**, red lead on pin 1 and black lead on pin 2. On copy B, the first and second transistors are Q101 and Q102. The two base connections are intentionally duplicated on each copy; the two emitter connections are different nodes. Neither emitter is GND.

**These are measurement headers, not jumper links: do not fit shorting caps.** Use COM and V/ohm meter sockets, not current mode across a header. The circuit operates normally without measurement leads. Power goes to J1/J101; the internal VCC at J2/J102 is after the input resistor/diode.

Across the nominal 1 kohm load, `Iout = Vload / 1000`; 5.00 V corresponds to 5.00 mA. Copy A's load is R6; copy B's is R106. The latest supplied simulation predicts about 4.625-4.667 mA over 25-75 C, not exactly 5 mA.

## Components per copy

| Copy A / B | Value / component |
|---|---|
| R1 / R101 | 1 ohm, 1/4 W resistor, not a fuse |
| R2 / R102 | 662 ohm, 1/4 W (LT Rs) |
| R3 / R103 | 1 kohm, 1/4 W |
| R4,R5 / R104,R105 | 22 ohm, 1/4 W, emitter-to-ground resistors |
| R6 / R106 | 1 kohm, 1/4 W load |
| R7 / R107 | Fixed nominal 120 ohm, 1/4 W; no trimmer |
| D1,D2 / D101,D102 | 1N4148 |
| D3 / D103 | BZX55C5V1 5.1 V Zener |
| D4 / D104 | 1N4007 series input diode |
| Q1,Q2 / Q101,Q102 | 2N3904 |
| C1 / C101 | 1.33 nF, at least 25 V |
| J1..J4 / J101..J104 | Four 2-pin male headers |

The 117.6 ohm measurement was reported for the **original supplied 120 ohm resistor**. It is retained as source context, not proof that the second resistor has the same measured resistance. Measure each assembled copy's actual parts separately. Two populated copies require twice the electronic components and eight headers total; a single set of inventory parts is insufficient for both.

## Files, checks and history

- [PCB README](PCB%20layout/README.md): detailed handoff and reproduction commands.
- [Panel component list](PCB%20layout/panel_BOM.csv) and [panel component data](PCB%20layout/panel_components.json): both copies and all header nets.
- [Panel audit](PCB%20layout/reports/panel_audit.json): fit, isolation, node mapping and CAD validation.
- [P4 change record](PCB%20layout/reports/P4_dual_panel_2026-10-30/README.md).
- [Panel hashes](PCB%20layout/reports/panel_sha256.json): design and printing artifacts.
- [Original LTspice files](schematics/): source circuit and user-supplied results, preserved.
- `PCB layout/Project.pretty`: local footprints required by both projects.

Checks cover the header unit and two-copy panel: ERC, DRC, zero unconnected items, schematic parity, native netlist-to-pad agreement, unique identifiers, 36 footprints, 24 separate nets and no shared ground. Standard configured checks are listed in the reports; no exclusions were added to hide layout problems. No physical board measurement or new SPICE simulation has been performed.

The supplied LTspice log reports 4.624594 mA at 25 C and 4.667352 mA at 75 C for 9.8 V, Rs=662 ohm, C1=1.33 nF and RV=117.6 ohm. Physical results depend on real parts and temperature matching. Warm uniformly and measure actual temperatures if testing thermal behaviour; stay within every actual part's ratings.

Historical P0/P1/P2/P3 reports, old trimmer footprints and the trimmer fitting template are retained for provenance only. Current projects contain no TP components or trimmers. The P1 geometry and P3 value-only helpers are retired to prevent restoring obsolete designs.

## Print and fabricate

Two **B.Cu-only, 1:1** PDFs are prepared:

- [Unmirrored copper](PCB%20layout/fabrication/dual_panel_BCu_unmirrored_1to1.pdf)
- [Mirrored copper](PCB%20layout/fabrication/dual_panel_BCu_mirrored_1to1.pdf)

**Ask college staff which orientation and mask polarity their transfer/photoresist process requires.** Both files show black where copper is to remain; a process needing reversed exposure polarity requires the lab's appropriate inversion. Print only the chosen variant, at **Actual Size / 100%**, with no fit-to-page scaling. Measure the **50 mm calibration line** after printing. The copper blank occupies a 150 x 100 mm rectangle; annotations/calibration are outside that rectangle and must not be transferred onto the board.

Do not print assembly or copper-review drawings as masks: they include borders and guides. The two mask variants contain no outline, silkscreen or cut guide in the copper artwork. Etching alone does not produce white component labels; use the assembly guide and mark headers during assembly.

Before fabrication, verify actual transistor manufacturer pinout (**CAD 1=E, 2=B, 3=C**), lead forming, resistor fit, C1's assumed 5 mm pitch and header fit. No extra fuse was added. Keep the two copies' supply leads separate if on-board isolation is to be maintained externally.
