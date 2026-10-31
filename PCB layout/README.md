# P8 rectangle pads with P6 placement, routing and retained cutting setup; header-equipped unit and two-copy 150 x 100 mm panel

**Open `dual_current_mirror.kicad_pro` / `dual_current_mirror.kicad_pcb` for the complete two-copy panel.** `current_mirror.kicad_pro` remains the reusable single 78 x 67 mm unit. KiCad 10.0.7 or later is required. In PCB Editor, press **Alt+3** for 3D. The shared project-local library is `Project.pretty` via `fp-lib-table`.





## P8: plain rectangle pad trial for CopperCAM

**Only pad outlines change; P6 component positions, labels, routes, hole centres, hole diameters and electrical connections are preserved.** The 20 oval pads (all 12 transistor pins plus 8 header pin-2 lands) and 8 rounded-rectangle diode lands are now plain rectangles with the same overall dimensions. The panel now has **36 rectangular and 40 circular pads**, with no oval pads, rounded-rectangle pads, aperture macros or filled pad regions in the copper Gerber. All 76 pads are standard aperture flashes. Existing circular pads remain circular.

Transistor lands remain 1.7 x 2.4 mm with 0.8 mm holes and 2.54 mm pitch. Header lands remain 2.4 x 1.7 mm with 1 mm holes and 2.54 mm pitch. Adjacent-land spacing remains 0.84 mm. **All transistor pins and both pins of each header are rectangular now: pad shape no longer identifies pin 1.** Use the numbered pins, transistor body orientation and assembly +/B/E/GND labels. Transistor numbering remains 1=emitter, 2=base, 3=collector.

This follows [Aalto Fablab's CopperCAM guidance](https://wiki.aalto.fi/spaces/AF/pages/362916083/Creating%2BTool%2BPaths%2Bwith%2BCopperCAM%2B-%2Bfor%2BBungard%2BCCD%2BMilling%2BMachine), which recommends circle/rectangle pads and reports recognition problems with oval and rounded-rectangle shapes. The previous oval-pad export was valid Gerber but was not confirmed compatible with the lab's CopperCAM. This trial is **not yet confirmed in that installation**. KiCad checks and export comparisons cannot substitute for that import test.

For the lab test, extract **`fabrication/dual_panel_coppercam_rectangles.zip` into a fresh folder** and start a fresh CopperCAM circuit from its `dual_current_mirror-B_Cu.gbr`. This avoids confusing the new file with an old extraction or cached job. Before calculating contours, check that all 12 transistor lands are visible, along with the header and diode lands. Then import the original-format drill file and verify registration using the known layer-1/layer-5 workflow. Do not assume the issue is fixed until this actual import is checked.

The standard manufacturing ZIP is also refreshed with identical contents. The 1.7 mm thickness and existing centre-cut setup are retained. Setup JSON still is not executable machine code. Generated previews show the new rectangles; the supplied screenshot preserves the P6 placement/routing view but predates the rectangle-pad trial. See `reports/coppercam_pads.json` and `reports/layout_restore.json` for the exported-pad and retained-layout checks.


## Retained P6 placement/routing and cutting setup

The recent header-spacing trial has been undone. The saved P6 component positions, labels and exact routing remain restored directly, not rerouted: J2/J4 and J102/J104 are back at their original positions, with 50 track segments in the unit and 100 in the panel. The straight/45-degree routes and centre-cut line remain; P8 changes pad outlines to rectangles as described above. Current project preferences, the 1.7 mm CAD thickness, supplied cutting parameters and replacement screenshot are retained. See `reports/layout_restore.json` for the exact-layout comparison.

The CAD board thickness is now **1.7 mm**, matching the user's reported blank. Centre-cut setup data records **Roland monoFab SRM-20**, **0.8 mm cutting diameter** and **0.4 mm maximum depth per pass**. Nominal planning depths below the top surface are **0.4, 0.8, 1.2, 1.6 and 1.7 mm**, ending at nominal board bottom. A full cut may require a confirmed breakthrough allowance into a sacrificial board. This is not an executable machine program: feed/plunge rates, spindle speed, Z-zero, safe clearance, cutter type/flute length, holding, breakthrough and output format still require operator confirmation.

The centre-cut line remains at x=75 mm. With a centred 0.8 mm kerf and no outer trimming, each separated half is nominally **74.6 x 100 mm**. Setup data is in `centre_cut_setup.json` and copied into the regenerated manufacturing ZIP. Read `reports/header_space.json` for geometry checks. The supplied P6 screenshot below matches placement and routing; generated previews show the P8 pad outlines.


## P6: straight routes, emitter pads and centre separation

The restored P6 layout uses horizontal, vertical and 45-degree track sections: **100 panel segments instead of 542**, with no track arcs or tiny staircase routes. Tracks remain **0.6 mm** wide with **0.8 mm minimum different-net clearance**. Standard rounded pad boundaries and tool-radius compensation may still produce arcs in CAM; these are different from jagged copper routing.

P6 used oval emitter lands on **Q1, Q2, Q101 and Q102**; P8 replaces all transistor lands with rectangles. Pin 1 remains the emitter. Land dimensions (1.7 mm along the pin row, 2.4 mm across it), 0.8 mm drills, 2.54 mm pin pitch and at least 0.45 mm annular copper are retained. All four emitter lands were present as rectangles in the previous PCB and Gerber; the reported disappearance was not reproduced in the source files. Their current rectangular flashes are explicitly checked in `reports/emitter_routes.json`. Confirm all four lands remain visible and intact in CopperCAM's generated isolation toolpaths before machining.

A separate **`dual_current_mirror-Centre_Cut.gbr`** contains one straight centreline at **x=75 mm, from y=0 to 100 mm**. It is exported from User.1, not copper or Edge.Cuts. This allows the 150 x 100 mm panel to be separated into two nominal 75 x 100 mm boards; the cutter removes a kerf, so finished widths will be slightly smaller. With a centred 1 mm kerf and no additional trimming, each width would be 74.5 mm. The cut centreline has at least 5.4 mm conservative clearance from circuit copper.

The centre-cut Gerber is **geometry only, not executable machine code**. The operator must assign a centreline cut-through operation, suitable cutter, actual measured board thickness, passes, feeds/speed, safe Z, output format and work holding. No tabs or depths are encoded. Copper isolation and drilling should precede final separation, with both halves secured. At P6, the model and board thickness were pending. P7 records the supplied SRM-20 model and 1.7 mm thickness; remaining machine settings are still pending.

The user resolved the earlier CopperCAM drill alignment by adjusting **layers 1 and 5**, using the original files. The experimental Excellon/Gerber drill files were deleted and are not restored. Use the latest regenerated ZIP for the restored P6 layout and inspect alignment and emitter lands after loading it.


## Earlier P5 hand-soldering clearance update (2026-10-31)

Both copies now use **0.8 mm minimum copper clearance**, with **0.6 mm tracks**. Header and transistor pin pitch remains **2.54 mm**. Their elongated pads are **1.7 mm along the pin row and 2.4 mm across it**, increasing the adjacent-pad gap from **0.54 to 0.84 mm**, while retaining soldering area. Header drills remain 1.0 mm; transistor drills remain 0.8 mm. Minimum copper around the holes is 0.35 mm for headers and 0.45 mm for transistors.

D1/D2 and D101/D102 were repositioned to spread the closely grouped diode joints. The two neighbouring diode-pad gaps are now **1.56 mm and 2.18 mm**. Those diode pairs are intentionally connected by the circuit; the 0.8 mm rule protects copper on different nets. Transistor outline graphics are on the assembly layer so they do not overlap the elongated lands.

The complete panel remains **150 x 100 mm**, with two isolated circuits. Electrical values, header functions, transistor pin numbering and hole diameters are preserved. There is no solder mask: use small amounts of solder and inspect for bridges. Use the regenerated ZIP for the restored P6 appearance and retained cutting setup. See `reports/solder_clearance.json` and `reports/P5_solder_clearance_2026-10-31/README.md`.


## Hardware change

The earlier six TP pads are removed. Every copy now has one power header and three measurement headers, all **1x2 male, 2.54 mm pitch**, with elongated 2.4 x 1.7 mm copper pads and 1 mm drills. Solder the pins on the copper side; attach female jumper leads above. Pads/holes are still needed to solder the pins. Do not fit shorting caps.

| Function | Copy A | Copy B | Pin 1 / red (use numbering/labels) | Pin 2 / black |
|---|---|---|---|---|
| 9.8 V power | J1 | J101 | VIN | GND |
| Rload voltage | J2 | J102 | VCC | OUT |
| Q1-role base-emitter | J3 | J103 | BASE | E1 |
| Q2-role base-emitter | J4 | J104 | BASE | E2 |

Copy B transistor names are Q101/Q102. Base nodes are common only within a copy; E1 and E2 remain separate and are not ground. Use DC voltage mode and COM/V-ohm sockets. Voltage across J2/J102 divided by nominal 1000 ohm gives load current. No meter is needed for normal operation. J1/J101 are the supply inputs; J2/J102 VCC is the internal supply after R1/D4.

## Panel construction

Each unit is rotated 90 degrees to 67 x 78 mm. Copy A bounds are (5.5,11)..(72.5,89) mm; copy B bounds are (77.5,11)..(144.5,89) mm. The blank is 150 x 100 mm, with a 5 mm unit gap, 5.5 mm side margins and 11 mm top/bottom margins.

The panel has **36 components, including 8 headers / 16 header pins**, and **24 nets in two disjoint groups**. A_ and B_ nets do not share power, ground, copper or component terminals. Shared external supplies/instruments may connect them externally. The User.1 centreline at x=75 mm exports separately as Centre_Cut.gbr; the operator sets up the final cutting operation. Both copies can stay on the same blank.

Tracks are 0.6 mm on B.Cu, minimum configured clearance 0.8 mm, no vias/jumpers/pours. Only the outer 150 x 100 mm boundary is Edge.Cuts. Through-hole pads appear on both layers in the data model; no front tracks are fabricated.

Supplied KiCad screenshot showing retained P6 placement and routing, before the P8 pad-shape change; current previews are in `previews/`:

![Supplied KiCad dual current-mirror PCB layout](Screenshot%202026-10-31%20121807.png)

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
- `reports/P8_rectangles_2026-10-31/README.md`: current handoff; earlier reports and trimmer templates are historical.

Both projects pass native ERC/DRC with zero reported violations, unconnected items or schematic parity issues. The independent audit verifies header roles, all panel pads against the exported netlist, rotations, fit, isolated grounds, unique UUIDs and bottom-only tracks. Standard ignored check categories are listed in native reports; no new exclusions were added.

## Milling or copper printing

For the college's **PCB milling machine + automated drilling**, use `fabrication/dual_panel_machine_files.zip` or the files under `fabrication/machine_files/`:

- **`dual_current_mirror-B_Cu.gbr`**: the only copper print layer.
- **`dual_current_mirror.drl`**: matched Excellon drill program, 76 holes.
- **`dual_current_mirror-Edge_Cuts.gbr`**: optional 150 x 100 mm outer outline; not copper artwork.
- **`dual_current_mirror-Centre_Cut.gbr`**: optional centreline separation cut at x=75 mm; operator sets depth/passes and holding; not copper artwork.

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
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\check_emitter_routes.py'
```

The source checker also reads installed LTspice symbol files. Process-only execution-policy settings do not change Windows' persistent policy. Registry/font-cache warnings can occur under restricted execution; inspect the actual JSON reports. Saved boards need no background Python process. Historical trimmer/value-only helpers are retired so they cannot silently restore obsolete revisions.
