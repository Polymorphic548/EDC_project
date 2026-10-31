> Historical trial: the user subsequently requested an exact P6 appearance restoration. The header move and its routes have been reverted; cutting setup data was retained. See `../P6_restored_2026-10-31/README.md`.

# P7 handoff - 2026-10-31

## P7: more room around the upper measurement headers

**J2/J4 in copy A and J102/J104 in copy B have moved 5 mm down**, with labels moved to match. A routing keep-out strip above them prevents passing tracks from moving back into that space. The measured vertical gap from the upper pad edge to passing track copper is **3.60 mm for J2/J102 and 5.11 mm for J4/J104**. The 2.54 mm connector pitch, pad dimensions, drill sizes and pin functions are unchanged. Tracks remain 0.6 mm wide with 0.8 mm minimum different-net clearance, using straight/45-degree sections (114 segments across the panel). All four emitter lands remain oval and explicitly checked in the Gerber.

The CAD board thickness is now **1.7 mm**, matching the user's reported blank. Centre-cut setup data records **Roland monoFab SRM-20**, **0.8 mm cutting diameter** and **0.4 mm maximum depth per pass**. Nominal planning depths below the top surface are **0.4, 0.8, 1.2, 1.6 and 1.7 mm**, ending at nominal board bottom. A full cut may require a confirmed breakthrough allowance into a sacrificial board. This is not an executable machine program: feed/plunge rates, spindle speed, Z-zero, safe clearance, cutter type/flute length, holding, breakthrough and output format still require operator confirmation.

The centre-cut line remains at x=75 mm. With a centred 0.8 mm kerf and no outer trimming, each separated half is nominally **74.6 x 100 mm**. Setup data is in `centre_cut_setup.json` and copied into the regenerated manufacturing ZIP. Read `reports/header_space.json` for geometry checks. The supplied screenshot below is P6, before this header move; generated previews show the current P7 layout.

## Scope and verification

Only the circled J2/J4 headers and their copy-B counterparts move; remaining component lead centres, values, pin nets and drill sizes are preserved. R6/R106 reference labels move to avoid overlap. Existing emitter-pad and straight-route checks are retained. Native ERC/DRC/parity, exact schematic-to-board nets, isolated grounds, manufacturing geometry, upper header clearance, physical model thickness and setup-file contents are checked. The source LTspice files are preserved.

The user's replacement screenshot is linked from the root and PCB READMEs. It shows P6; generated current previews show P7. The local pre-P7 snapshot is in the ignored `current_mirror-backups/before_P7_header_space_2026-10-31/` folder. The earlier P5/P6 reports are historical.
