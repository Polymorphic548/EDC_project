# PCB milling + automated drill: P5 dual panel

This job is for a **150 x 100 mm, single-copper-sided board**, carrying **two electrically independent current mirrors**.

## Load these two files

| Operation | File |
|---|---|
| Copper geometry to retain (CAM generates milling paths) | **dual_current_mirror-B_Cu.gbr** |
| Drill the component/header holes | **dual_current_mirror.drl** |

`dual_current_mirror-Edge_Cuts.gbr` is the **optional board outline / dimensional reference**, not another copper layer. Do not print it as copper. The internal centre guide is not an outline or slot and is not exported.

`dual_current_mirror-drl_map.pdf` and `drill_report.rpt` are reference documents for checking drill tools and locations; they are not machine drill programs. `verification.json` records the export-to-PCB checks and `SHA256.json` identifies the files.

## P5 soldering clearance and milling

Tracks are 0.6 mm wide. Minimum clearance between different nets is 0.8 mm. Header/transistor lands have 0.84 mm between adjacent pads at unchanged 2.54 mm pitch. Their pad dimensions are 1.7 mm along the pin row and 2.4 mm perpendicular to it. Hole diameters remain 0.8, 1.0 and 1.1 mm (56, 16 and 4 holes respectively).

For the college milling machine, generate isolation toolpaths around the copper features to retain. These Gerbers are geometry inputs, not G-code. The operator selects tools, depth, feeds, fixture and copper-side transformation, and checks tool clearance in CAM. The optional outline is a separate board-cutting operation; do not mill it as a copper-isolation feature. No automatic centre cut is included. Milling leaves unused copper outside isolation channels unless the operator requests area clearing.

If using a direct resist printer instead, the same copper image describes protected copper and the board is then etched. The printing/polarity notes below apply to that alternative.

## Machine setup

- Gerber is standard **RS-274X**, absolute coordinates, millimetres, 4.6 coordinate format, positive copper image. Excellon is absolute, metric, explicit decimal coordinates.
- Both use the **same absolute origin and the same unmirrored CAD orientation**. KiCad expresses physical board Y-down as Cartesian negative Y in both exports. Do not mirror, offset or scale only one of the two files: they must remain registered. Let the machine operator configure the copper-side loading/fixture transform for the pair.
- Manufacture/print **B.Cu only**. There is no F.Cu artwork in this package. F.Cu being visible/selected in the editor, or through-hole pads appearing on both sides of the KiCad model, does not require a second physical copper face.
- Print on the one copper-coated face. Components mount from the opposite face, with through-hole pins soldered to the printed/etched copper face.
- Copper artwork is at **1:1**. The optional outline is exactly **150 x 100 mm**. Confirm machine units and placement before printing/drilling.
- Dark Gerber features denote copper to keep/protect. Confirm how the machine interprets resist/ink polarity; do not invert without the operator checking the process.
- All holes are ordinary through-drilled component/header holes for this single-sided assembly. KiCad's PTH annotations describe the footprint model; **no plated barrels or second copper layer are requested**.

Copy A and B share no copper, power or ground. A shared external supply/instrument can join them externally. No white silkscreen, text, soldermask layer, or measurement-header jumper cap is part of this copper print job.

The approved design uses two 9.8 V inputs, 662 ohm reference resistors, 1.33 nF capacitors and fixed nominal 120 ohm bias resistors. Refer to the separate assembly drawing for component orientation and header pin functions. Physical fit and actual transistor pinout still need assembly checks.
