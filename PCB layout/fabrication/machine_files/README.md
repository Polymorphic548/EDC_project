# PCB milling + automated drill + optional centre cut: P8 rectangle pad trial; P6 routes and retained cutting setup

This job is for a **150 x 100 mm, single-copper-sided board**, carrying **two electrically independent current mirrors**.

## Manufacturing inputs

| Operation | File |
|---|---|
| Copper geometry to retain (CAM generates milling paths) | **dual_current_mirror-B_Cu.gbr** |
| Drill the component/header holes | **dual_current_mirror.drl** |
| Optional straight centre separation, as its own centreline cutting job | **dual_current_mirror-Centre_Cut.gbr** |

`dual_current_mirror-Edge_Cuts.gbr` is the **optional board outline / dimensional reference**, not another copper layer. Do not print it as copper. The full-length centreline is exported separately in `dual_current_mirror-Centre_Cut.gbr`; it is not part of copper, drills or outer outline.

`dual_current_mirror-drl_map.pdf` and `drill_report.rpt` are reference documents for checking drill tools and locations; they are not machine drill programs. `verification.json` records the export-to-PCB checks and `SHA256.json` identifies the files.

## P8 rectangle pads with retained P6 placement/routing

The 5 mm header movement has been undone. J2/J4 and J102/J104 are at their saved P6 positions, with the exact saved P6 routes and labels restored. Connector pitch and hole diameters are preserved. Cutting setup data is retained.

Tracks are 0.6 mm wide. Minimum clearance between different nets is 0.8 mm. Header/transistor lands have 0.84 mm between adjacent pads at unchanged 2.54 mm pitch. Their pad dimensions are 1.7 mm along the pin row and 2.4 mm perpendicular to it. All transistor and header lands are rectangular; the eight former rounded-rectangle diode lands are also plain rectangles. Other circular lands stay circular. Pin 1 is identified by numbering and assembly labels, not by a unique pad shape. All copper tracks are straight horizontal/vertical/45-degree sections (100 segments total), with no track arcs or tiny staircase routes. Inspect emitter lands and the generated isolation paths in CAM. Hole diameters remain 0.8, 1.0 and 1.1 mm (56, 16 and 4 holes respectively).

For the college milling machine, generate isolation toolpaths around the copper features to retain. These Gerbers are geometry inputs, not G-code. The operator selects tools, depth, feeds, fixture and copper-side transformation, and checks tool clearance in CAM. The optional outline is a separate board-cutting operation; do not mill it as a copper-isolation feature. The separate centre-cut geometry is included; depth, passes, holding and machine code are not included. Milling leaves unused copper outside isolation channels unless the operator requests area clearing.

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

## Optional centre separation

`dual_current_mirror-Centre_Cut.gbr` has exactly one open straight path: x=75 mm, y=0 to -100 mm in Gerber Cartesian coordinates. Its 0.1 mm display stroke is **not a specified cutter diameter**. Import it as a separate centreline cutting operation; do not engrave isolation around it or treat it as a second copper layer. An outline routine requiring a closed contour must not close this path through the circuitry. The operator must generate an appropriate centreline toolpath using the cutting tool, rather than the copper-isolation engraving tool.

Keep the copper, drill, outline and centre-cut geometry in the same registered frame. Do not independently reframe/centre the cut file: it has no pads for reference-pad alignment. If CopperCAM repositions imported layers, the operator must position this line at the physical panel midpoint and verify it runs between the two copies before generating any cutting motion.

The uncut panel is 150 x 100 mm. Each nominal half is 75 x 100 mm before kerf; for a centred cutter of diameter d, the untrimmed half width is (150-d)/2 mm. The cut centreline is at least 5.4 mm from copper. Copper isolation and drilling precede centre separation. Both halves require secure support/work holding; no holding tabs are encoded.

This file contains no cutting depth, pass depth, feed, spindle speed, safe Z or machine commands. User-provided values are now recorded: SRM-20, 1.7 mm board, 0.8 mm cutting diameter, 0.4 mm maximum pass depth. The CAD thickness is also 1.7 mm. Feed/plunge rates, spindle speed, Z-zero, safe Z, cutter type/flute length, holding, breakthrough allowance and machine output format remain pending.

The earlier alignment issue was resolved by the user using CopperCAM layers 1 and 5, not by the trial drill files. Those trial files are not included. Confirm full registration and dimensions with this fresh package.

## Recorded centre-cut setup

`centre_cut_setup.json` is setup data only, not machine code. The nominal depths to board bottom are 0.4, 0.8, 1.2, 1.6 and 1.7 mm below the top surface. An operator-confirmed breakthrough allowance may be required for full separation. With the supplied 0.8 mm cutter, the two untrimmed halves would each be about 74.6 x 100 mm after a centred kerf. No SRM-20 RML/G-code program has been issued.

## CopperCAM import trial

This package uses only standard Gerber **C and R apertures** for the copper pads: 36 rectangular, 40 circular. No O apertures, aperture macros or G36/G37 filled pad regions remain. All 12 transistor lands are explicit R flashes; their positions, dimensions, drills and the P6 routes are unchanged.

Use a fresh extraction and a fresh CopperCAM circuit, loading B_Cu.gbr as the circuit copper. Check all 12 transistor lands and the header/diode lands immediately on import, before calculating contours. CopperCAM confirmation is still pending; file checks do not prove compatibility with the lab installation. The standard and clearly named rectangle-trial ZIPs contain the same manufacturing files. Retain the established layer-1/layer-5 drill alignment workflow.
