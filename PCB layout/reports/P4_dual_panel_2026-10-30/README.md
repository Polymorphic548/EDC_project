# P4: two independent circuits and plug-in measurement headers

The user authorized replacing the loose TP pads with male/female wire attachment points and fitting two isolated copies to their 15 x 10 cm copper blank.

## Implemented

- Reusable 78 x 67 mm unit retains the P3 electrical values and all core components.
- TP1..TP6 removed from the active schematic/PCB.
- J1 power header retained; J2 load-voltage, J3 Q1 base-emitter and J4 Q2 base-emitter headers added. All are two-pin 2.54 mm straight male headers, with 2 mm pads and 1 mm holes.
- Unit rerouted on B.Cu with 0.6 mm tracks; no vias or jumpers.
- Two rotated 67 x 78 mm units placed on a 150 x 100 mm panel, with 5 mm between unit rectangles, 5.5 mm side margins and 11 mm top/bottom margins.
- Flat panel schematic has A_ and B_ namespaces. Copy B reference numbers add 100, so both schematics and PCB have unique references.
- Copper-only mirrored and unmirrored 1:1 PDFs prepared. Both are positioned in the same 150 x 100 mm rectangle by translation, not scaling. College staff must select orientation and polarity.

The primary project is now `dual_current_mirror.kicad_pro`. The original `current_mirror` project remains the reusable header-equipped unit, not the full panel.

## Verified

Native unit and panel ERC/DRC report no violations, unconnected items or schematic parity issues. The independent panel audit verifies 36 components, 8 headers, 24 nets, unique UUIDs, unit rotations/positions, all pad nets against the native exported netlist, and no shared ground or power net. Actual group copper bounding boxes are separated by approximately 12.98 mm horizontally, exceeding the 5 mm unit-frame gap.

The requested measurement pin maps are:

| Copy A / B | Pin 1 | Pin 2 |
|---|---|---|
| J1 / J101 | VIN | GND |
| J2 / J102 | VCC | OUT |
| J3 / J103 | BASE | E1 |
| J4 / J104 | BASE | E2 |

E1/E2 are transistor emitters above their respective 22 ohm resistors, not ground. Pin 1 is the square pad and positive/red voltage lead. Measurement headers are not shorting-jumper locations.

Machine-readable evidence: `../panel_audit.json`, `../panel_erc.json`, `../panel_drc.json`, `../board_audit.json`, `../source_connectivity.json` and `../panel_sha256.json`. This is CAD validation, not a physical board measurement or safety-rated isolation qualification. A shared external supply or grounded instrument can connect the copies externally.

Two populated copies need twice the circuit inventory plus eight headers total. The original resistor's reported 117.6 ohm value is not evidence that a second 120 ohm part measures identically. Actual part fit, manufacturer's transistor pinout, capacitor lead pitch, printing scale and college transfer requirements still need physical confirmation. No new LTspice run or hardware test was performed.
