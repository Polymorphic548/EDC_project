# Restored P6: choose the correct 1:1 copper artwork

## College PCB milling / automated drill workflow

Use `dual_panel_machine_files.zip`, or open `machine_files/README.md` for the individual machine inputs. The copper file is **`dual_current_mirror-B_Cu.gbr`**; the drill file is **`dual_current_mirror.drl`**. Load these as a registered pair in millimetres. No F.Cu print layer is needed. `Edge_Cuts.gbr` is a separate optional boundary reference, not another print layer. For milling, import the Gerber as copper to retain and let the operator generate isolation toolpaths; this is not G-code. Minimum different-net clearance is 0.8 mm, tracks 0.6 mm. The PDF instructions below are for the alternative paper/film method. Use the regenerated restored-P6 ZIP rather than an older download.

## Paper / film transfer alternatives

For the **150 x 100 mm dual-copy panel**, use exactly one of:

- `dual_panel_BCu_unmirrored_1to1.pdf`
- `dual_panel_BCu_mirrored_1to1.pdf`

Ask college staff which orientation matches their contact/transfer method. Both show black copper to keep; a process needing inverse exposure polarity requires the lab's correct inversion. These are copper-only plots, without outline or assembly/cutting-guide graphics in the board area.

Print **Actual Size / 100%** on A4 landscape; disable all fit/shrink scaling. Verify the separate **50 mm calibration line**. The 150 x 100 mm board area starts at the page's top-left origin; labels and calibration are BELOW that area and must not be transferred onto the copper blank. The mirrored variant has been translated from KiCad's page-centred mirror position to the same board area, with no scaling.

Use the assembly preview separately to identify headers/components. White labels are not created by chemical copper etching. No jumper caps belong on the measurement headers.

Before etching/drilling, confirm actual component lead fit and transistor pinout. The two circuits have no common copper/ground, but wiring them to a shared supply or common-ground instrument may connect them externally. The optional Centre_Cut.gbr provides the full-length centre separation path. It is excluded from these copper-only PDFs; the operator must configure a separate cut-through centreline job.

For optional centre separation, see `machine_files/README.md`. The new centre-cut Gerber is not a copper layer and must not be included in a copper mask. It contains no depths or machine program.
