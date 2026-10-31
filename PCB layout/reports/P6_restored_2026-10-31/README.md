# Exact P6 PCB appearance restored - 2026-10-31

The user requested undoing only the recent header movement and its rerouting. The unit and panel PCB files were restored from the pre-P7 snapshot, rather than rerouted. Footprint positions, every track, graphical labels, pad shapes, model positions, UUIDs and centre-cut drawing are compared with that snapshot. The restored boards retain the current 1.7 mm physical thickness; project preferences and centre-cut setup data remain unchanged.

The current layout has 50 straight/45-degree track sections per unit, 100 on the panel. The upper measurement headers are back at panel y=19 mm, with original 2.54 mm pitch and original pads/drills. All four emitter lands retain the P6 oval shape. The optional x=75 mm separation line remains.

Retained cutting setup: monoFab SRM-20; user-reported 1.7 mm thickness, 0.8 mm cutter and 0.4 mm maximum depth per pass. Nominal depths to board bottom are 0.4, 0.8, 1.2, 1.6 and 1.7 mm. Remaining feed, spindle, Z-zero, safe clearance, tool/holding, breakthrough and machine-format confirmations are still required. The setup JSON is unchanged; no executable cutting code is generated.

The replacement screenshot and updated README content are retained, with current captions corrected. Manufacturing copper, drill, outline, centre-cut geometry, PDFs and ZIP are regenerated to match the restored board. Native ERC/DRC/parity and existing netlist/isolation/geometry checks are rerun. See `../layout_restore.json` for exact-layout fingerprints.
