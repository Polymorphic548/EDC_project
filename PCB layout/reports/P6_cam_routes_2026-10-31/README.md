# P6 handoff - 2026-10-31

## P6: straight routes, emitter pads and centre separation

The current layout uses horizontal, vertical and 45-degree track sections: **100 panel segments instead of 542**, with no track arcs or tiny staircase routes. Tracks remain **0.6 mm** wide with **0.8 mm minimum different-net clearance**. Standard rounded pad boundaries and tool-radius compensation may still produce arcs in CAM; these are different from jagged copper routing.

The emitter lands of **Q1, Q2, Q101 and Q102** are now **oval**, matching their base/collector lands. Pin 1 remains the emitter. Land dimensions (1.7 mm along the pin row, 2.4 mm across it), 0.8 mm drills, 2.54 mm pin pitch and at least 0.45 mm annular copper are retained. All four emitter lands were present as rectangles in the previous PCB and Gerber; the reported disappearance was not reproduced in the source files. Their new oval flashes are explicitly checked in `reports/emitter_routes.json`. Confirm all four lands remain visible and intact in CopperCAM's generated isolation toolpaths before machining.

A separate **`dual_current_mirror-Centre_Cut.gbr`** contains one straight centreline at **x=75 mm, from y=0 to 100 mm**. It is exported from User.1, not copper or Edge.Cuts. This allows the 150 x 100 mm panel to be separated into two nominal 75 x 100 mm boards; the cutter removes a kerf, so finished widths will be slightly smaller. With a centred 1 mm kerf and no additional trimming, each width would be 74.5 mm. The cut centreline has at least 5.4 mm conservative clearance from circuit copper.

The centre-cut Gerber is **geometry only, not executable machine code**. The operator must assign a centreline cut-through operation, suitable cutter, actual measured board thickness, passes, feeds/speed, safe Z, output format and work holding. No tabs or depths are encoded. Copper isolation and drilling should precede final separation, with both halves secured. Machine-ready depth/pass programming remains pending the actual monoFab model and operator setup; the 1.6 mm CAD model thickness is not a measurement.

The user resolved the earlier CopperCAM drill alignment by adjusting **layers 1 and 5**, using the original files. The experimental Excellon/Gerber drill files were deleted and are not restored. Use the regenerated P6 ZIP and inspect alignment and emitter lands after loading it.

## Verification

Both native KiCad projects are checked for ERC, DRC and schematic parity, with the existing 0.8 mm copper clearance enforced. Audits compare all part values, pad nets, hole diameters and pin centres with the pre-P6 snapshot, verify isolated copies, and check the actual exported emitter apertures and straight track angles. The package checker compares copper/drill/outer-outline/centre-cut geometry against the saved panel. No physical cut or CopperCAM toolpath validation has been performed here.

See `../emitter_routes.json`, `../panel_audit.json`, `../solder_clearance.json`, native reports, and the machine folder's `verification.json`. The local pre-edit snapshot is in the ignored `current_mirror-backups/before_P6_cam_routes_2026-10-31/` directory. Earlier P5 screenshots are historical; generated previews show P6.
