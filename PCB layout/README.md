# P4: header-equipped unit and two-copy 150 x 100 mm panel

**Open `dual_current_mirror.kicad_pro` / `dual_current_mirror.kicad_pcb` for the complete two-copy panel.** `current_mirror.kicad_pro` remains the reusable single 78 x 67 mm unit. KiCad 10.0.7 or later is required. In PCB Editor, press **Alt+3** for 3D. The shared project-local library is `Project.pretty` via `fp-lib-table`.

## Hardware change

The earlier six TP pads are removed. Every copy now has one power header and three measurement headers, all **1x2 male, 2.54 mm pitch**, with 2 mm copper pads and 1 mm drills. Solder the pins on the copper side; attach female jumper leads above. Pads/holes are still needed to solder the pins. Do not fit shorting caps.

| Function | Copy A | Copy B | Pin 1 / red / square pad | Pin 2 / black |
|---|---|---|---|---|
| 9.8 V power | J1 | J101 | VIN | GND |
| Rload voltage | J2 | J102 | VCC | OUT |
| Q1-role base-emitter | J3 | J103 | BASE | E1 |
| Q2-role base-emitter | J4 | J104 | BASE | E2 |

Copy B transistor names are Q101/Q102. Base nodes are common only within a copy; E1 and E2 remain separate and are not ground. Use DC voltage mode and COM/V-ohm sockets. Voltage across J2/J102 divided by nominal 1000 ohm gives load current. No meter is needed for normal operation. J1/J101 are the supply inputs; J2/J102 VCC is the internal supply after R1/D4.

## Panel construction

Each unit is rotated 90 degrees to 67 x 78 mm. Copy A bounds are (5.5,11)..(72.5,89) mm; copy B bounds are (77.5,11)..(144.5,89) mm. The blank is 150 x 100 mm, with a 5 mm unit gap, 5.5 mm side margins and 11 mm top/bottom margins.

The panel has **36 components, including 8 headers / 16 header pins**, and **24 nets in two disjoint groups**. A_ and B_ nets do not share power, ground, copper or component terminals. Shared external supplies/instruments may connect them externally. The centre guide at x=75 mm is drawing-layer documentation only; no slot or cut is manufactured automatically. Both copies can stay on the same blank.

Tracks are 0.6 mm on B.Cu, minimum configured clearance 0.4 mm, no vias/jumpers/pours. Only the outer 150 x 100 mm boundary is Edge.Cuts. Through-hole pads appear on both layers in the data model; no front tracks are fabricated.

## Electrical values and footprints

Per copy: input 9.8 V; Rs/R2=662 ohm; R3 and load R6=1 kohm; R1=1 ohm; emitter R4/R5=22 ohm; fixed R7=120 ohm nominal; C1=1.33 nF; 2N3904 pair; 1N4007 input diode; BZX55C5V1 Zener; two 1N4148 diodes. Resistors use quarter-watt axial footprints at 7.62 mm pitch; C1 uses 5 mm pitch. Transistors use the wide TO-92 footprint with 1=E, 2=B, 3=C. Verify physical parts before assembly.

Copy B references add 100: R1->R101, Q1->Q101, J1->J101, etc. The fixed resistor's reported 117.6 ohm measurement refers to the original part only; the duplicate CAD label carries source context, not a measured claim for a second part. Measure both physical copies separately. There is no trimmer, wiper, current-adjustment screw or added fuse.

The original LTspice topology is retained, with fixed R7 replacing its RV parameter. Source files are unchanged. Supplied results are 4.624594 mA at 25 C and 4.667352 mA at 75 C. CAD checks do not establish real current/temperature performance; no new simulation or physical measurement was performed.

## Files and validation

- `dual_current_mirror.kicad_*`: panel project, flat schematic with independent A_/B_ labels, and routed PCB.
- `panel_BOM.csv`, `panel_components.json`: both copies and their header pin maps.
- `current_mirror.kicad_*`, `BOM.csv`, `components.json`: reusable header unit.
- `previews/dual_panel_assembly.*`, `dual_panel_copper_review.*`, `dual_panel_schematic.*`: panel review drawings.
- `reports/panel_erc.json`, `panel_drc.json`, `panel_audit.json`, `panel_sha256.json`: panel checks, isolation audit and hashes.
- `reports/erc.json`, `drc.json`, `board_audit.json`, `source_connectivity.json`: unit checks.
- `reports/P4_dual_panel_2026-10-30/README.md`: current handoff; earlier reports and trimmer templates are historical.

Both projects pass native ERC/DRC with zero reported violations, unconnected items or schematic parity issues. The independent audit verifies header roles, all panel pads against the exported netlist, rotations, fit, isolated grounds, unique UUIDs and bottom-only tracks. Standard ignored check categories are listed in native reports; no new exclusions were added.

## Copper printing

For the college's **direct copper printer + automated drilling**, use `fabrication/dual_panel_machine_files.zip` or the files under `fabrication/machine_files/`:

- **`dual_current_mirror-B_Cu.gbr`**: the only copper print layer.
- **`dual_current_mirror.drl`**: matched Excellon drill program, 76 holes.
- **`dual_current_mirror-Edge_Cuts.gbr`**: optional 150 x 100 mm outline reference; not copper artwork.

The package includes a drill map, tool report, export verification, instructions and SHA-256 hashes. No front-copper file is supplied. F.Cu can be visible in the editor because pads are through-hole, while every routed track is B.Cu. The machine operator should load the copper and drill files together using their shared absolute origin and millimetre units; any fixture-side mirroring/positioning must be applied consistently to both. The physical panel remains single-sided; the KiCad hole-plating annotations do not request plated barrels.

To regenerate machine files, run `scripts/export_machine_files.ps1` with a process-only execution-policy override, then run `scripts/check_machine_files.py` with regular Python. This exporter produces standard RS-274X Gerber and metric decimal Excellon; the checker verifies all hole locations/sizes, pad shapes and tracks against the saved board. ZIP packaging is a convenience copy of that checked folder. CAD files are unchanged by export.

`fabrication/dual_panel_BCu_unmirrored_1to1.pdf` and `dual_panel_BCu_mirrored_1to1.pdf` contain **B.Cu only**, without outline, assembly graphics or centre guides. Both variants are normalized to the same 150 x 100 mm rectangle at the top left of an A4 landscape page, without scaling. Labels and a 50 mm calibration line are outside the blank area. Black denotes copper to keep.

Confirm mirror orientation and exposure polarity with college staff. Print the selected version at Actual Size / 100%, verify the 50 mm line, and transfer only the board area. A negative-polarity resist process may require the lab's inversion. Do not use review images/PDFs as masks. Chemical etching alone will not produce silkscreen labels; follow the assembly guide and label the connections manually as needed.

## Reproduce

Back up manual CAD edits before running generators. Existing unit project settings are preserved. A pre-P4 snapshot is stored locally in the ignored `current_mirror-backups/before_P4_panel_2026-10-30/` folder. Full generation recreates the header unit, then panelizes it. KiCad's bundled Python supplies pcbnew and NumPy; optional PNG generation uses the existing regular Python/PyMuPDF installation.

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\build_design.py'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\route_board.py'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\build_dual_panel.py'
```

Run `kicad-cli sch export netlist`, `sch erc --format json`, and `pcb drc --format json --schematic-parity` for **both** projects, writing the reports named above. Then:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\PCB layout\scripts\export_previews.ps1'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\PCB layout\scripts\export_panel_previews.ps1'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\check_design.py'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\check_dual_panel.py'
```

The source checker also reads installed LTspice symbol files. Process-only execution-policy settings do not change Windows' persistent policy. Registry/font-cache warnings can occur under restricted execution; inspect the actual JSON reports. Saved boards need no background Python process. Historical trimmer/value-only helpers are retired so they cannot silently restore obsolete revisions.
