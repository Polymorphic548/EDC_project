# P1: measured trimmer geometry update

The user's corrected measurements are applied to RV1:

| Feature | Dimension |
|---|---|
| Body diameter | 9 mm |
| Opposite pin pair | 8 mm centre-to-centre |
| Third pin | 5 mm from body centre, perpendicular to the opposite pair |
| Local hole centres in component-side CAD view | (-4,0), (+4,0), (0,+5) mm |
| Body centre on PCB | (49,38) mm |
| Copper pads / assumed drill diameter | 2.4 mm / 1.0 mm |

The body outline and courtyard are included in the project-local footprint `Project:RV1_D9_P8_Offset5_PINOUT_UNVERIFIED`. It replaces the active P0 2.54 mm-spaced placeholder. The old library item and P0 review remain historical records. No standard RM065 footprint was substituted.

## Physical pin assignment is still pending

The intended resistance is 500 ohm. The offset hole is provisionally pad 2; **this does not establish that the real offset terminal is the wiper**. The schematic's adjustable-resistor function still requires a wiper/end tie. Verify the loose part with a meter before fabrication and swap physical pad roles if needed. A pin-side view mirrors left and right compared with the component-side CAD view.

The 1 mm drill is an assumption based on the description of thin pins, not a measured lead diameter. Body height/model and resistance marking are not established. No guessed 3D body was added. Use the separate 1:1 fitting-template PDF and check its 50 mm calibration line before relying on the print.

**Meter check reported by the user:** A-B readings change, while A-C and B-C show "no value." It is not yet established whether the adjustment was moving, whether probe contact was reliable, or whether the display meant open circuit versus zero resistance. This does not identify the wiper or confirm the part is functional. No physical pin assignment was changed from these inconclusive readings.

## Layout and validation

The board remains 78 x 67 mm. RV1 fits inside the original reserved area; other component positions and circuit values are preserved. The board was rerouted on B.Cu with 0.6 mm tracks and no vias or jumpers.

Current machine-readable results are `../erc.json`, `../drc.json`, `../board_audit.json`, `../routing.json` and `../trimmer_geometry_2026-10-29.json`. They check CAD connectivity and geometry, not real wiper identity or physical circuit performance. Design/source hashes are refreshed in `../design_sha256.json` after checks.

The original design files and user-modified project preferences were backed up locally to the ignored `current_mirror-backups/before_P1_2026-10-29/` folder. Existing project preferences were retained. Reopen the PCB from disk to view P1; an already-open editor can still display its previous in-memory layout.
