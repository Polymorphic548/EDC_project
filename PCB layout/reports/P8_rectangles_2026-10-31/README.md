# P8 CopperCAM rectangle-pad trial - 2026-10-31

The user reports that all 12 transistor pads vanish immediately when CopperCAM opens the copper Gerber. All 12 are present in the valid previous file and share the O 2.4 x 1.7 mm aperture. Aalto Fablab documents problems recognizing oval/rounded-rectangle pads in CopperCAM. Changing emitters to oval in P6 was not validated in the target application. The likely compatibility explanation is not a locally reproduced root cause.

## P8: plain rectangle pad trial for CopperCAM

**Only pad outlines change; P6 component positions, labels, routes, hole centres, hole diameters and electrical connections are preserved.** The 20 oval pads (all 12 transistor pins plus 8 header pin-2 lands) and 8 rounded-rectangle diode lands are now plain rectangles with the same overall dimensions. The panel now has **36 rectangular and 40 circular pads**, with no oval pads, rounded-rectangle pads, aperture macros or filled pad regions in the copper Gerber. All 76 pads are standard aperture flashes. Existing circular pads remain circular.

Transistor lands remain 1.7 x 2.4 mm with 0.8 mm holes and 2.54 mm pitch. Header lands remain 2.4 x 1.7 mm with 1 mm holes and 2.54 mm pitch. Adjacent-land spacing remains 0.84 mm. **All transistor pins and both pins of each header are rectangular now: pad shape no longer identifies pin 1.** Use the numbered pins, transistor body orientation and assembly +/B/E/GND labels. Transistor numbering remains 1=emitter, 2=base, 3=collector.

This follows [Aalto Fablab's CopperCAM guidance](https://wiki.aalto.fi/spaces/AF/pages/362916083/Creating%2BTool%2BPaths%2Bwith%2BCopperCAM%2B-%2Bfor%2BBungard%2BCCD%2BMilling%2BMachine), which recommends circle/rectangle pads and reports recognition problems with oval and rounded-rectangle shapes. The previous oval-pad export was valid Gerber but was not confirmed compatible with the lab's CopperCAM. This trial is **not yet confirmed in that installation**. KiCad checks and export comparisons cannot substitute for that import test.

For the lab test, extract **`fabrication/dual_panel_coppercam_rectangles.zip` into a fresh folder** and start a fresh CopperCAM circuit from its `dual_current_mirror-B_Cu.gbr`. This avoids confusing the new file with an old extraction or cached job. Before calculating contours, check that all 12 transistor lands are visible, along with the header and diode lands. Then import the original-format drill file and verify registration using the known layer-1/layer-5 workflow. Do not assume the issue is fixed until this actual import is checked.

The standard manufacturing ZIP is also refreshed with identical contents. The 1.7 mm thickness and existing centre-cut setup are retained. Setup JSON still is not executable machine code. Generated previews show the new rectangles; the supplied screenshot preserves the P6 placement/routing view but predates the rectangle-pad trial. See `reports/coppercam_pads.json` and `reports/layout_restore.json` for the exported-pad and retained-layout checks.

## Validation boundary

Native KiCad ERC/DRC/parity are rerun with the existing rules. All pad centres, dimensions, drills, nets, component locations, tracks, labels, UUIDs and centre-cut geometry are compared with the saved P6 layout, permitting only the requested oval/roundrect-to-rect outline changes. Schmatics, project preferences and centre-cut setup are protected by hashes. Export checks require 76 standard C/R flashes, zero filled pad regions, zero aperture macros and explicit rectangles at all 12 transistor pins. The lab must still confirm the fresh import and resulting toolpaths.

The pre-edit snapshot is in the ignored `current_mirror-backups/before_P8_rectangles_2026-10-31/` folder. No experimental drill-format files are restored and no cutting program is generated. No source LTspice files are modified.
