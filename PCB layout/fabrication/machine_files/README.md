# Direct copper printer + automated drill: P4 dual panel

This job is for a **150 x 100 mm, single-copper-sided board**, carrying **two electrically independent current mirrors**.

## Load these two files

| Operation | File |
|---|---|
| Print the copper-protection pattern | **dual_current_mirror-B_Cu.gbr** |
| Drill the component/header holes | **dual_current_mirror.drl** |

`dual_current_mirror-Edge_Cuts.gbr` is the **optional board outline / dimensional reference**, not another copper layer. Do not print it as copper. The internal centre guide is not an outline or slot and is not exported.

`dual_current_mirror-drl_map.pdf` and `drill_report.rpt` are reference documents for checking drill tools and locations; they are not machine drill programs. `verification.json` records the export-to-PCB checks and `SHA256.json` identifies the files.

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
