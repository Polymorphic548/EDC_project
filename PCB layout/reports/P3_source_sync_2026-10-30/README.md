# P3: synchronize the updated LTspice values

The user updated the LTspice source and saved simulation results in commit `17bdbb4`. Comparing it with the previous source shows value and display changes only: wire geometry, flags, component symbols and reference names are unchanged. Reordering `InstName` and `Value` attributes on D4/Dz is not a component rename.

| Item | Previous | Updated |
|---|---|---|
| V1 / J1 input | 12 V | 9.8 V |
| Rs / PCB R2 | 620 ohm | 662 ohm |
| C1 | 100 nF | 1.33 nF |
| Source RV parameter | 119.8 ohm | 117.6 ohm |
| PCB R7 | 120 ohm nominal | Same fixed part; label now includes 117.6 ohm measured |

The fixed nominal 120 ohm resistor remains as previously requested; its reported 117.6 ohm measurement matches the updated source parameter. The trimmer is not restored. Existing KiCad component reference numbers are retained; the source-to-PCB reference mapping is unchanged.

The schematic, PCB value fields, input silkscreen label, BOM, component data and review previews are updated. **All tracks, pad geometry/net assignments, footprint IDs, placements and board outline are preserved. No routing operation was run.** `sync_source_values.py` asserts this before accepting the edit. The footprint library's value properties are synchronized without changing geometry.

Current check results are `../erc.json`, `../drc.json`, `../board_audit.json` and `../source_connectivity.json`. `changes.json` records the value edits; `checks.json` records the final preservation and validation assertions. `../design_sha256.json` identifies the current source and CAD files. The current layout remains 78 x 67 mm, B.Cu-only routing, with no vias/jumpers.

The user's supplied updated LTspice log reports **4.62459400296 mA at 25 C** and **4.66735195369 mA at 75 C**. These are source simulation results, not physical circuit measurements or a new run performed during this update. The original 5 mA title is a design target, not the updated measured/simulated result.

Physical component fit and college mask/printing requirements remain the same pre-fabrication checks. A local pre-update snapshot is retained under the ignored `current_mirror-backups/before_P3_source_sync_2026-10-30/` folder. Existing project preferences are preserved.
