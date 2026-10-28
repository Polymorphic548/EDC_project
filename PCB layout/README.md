# Single-layer 5 mA current mirror — provisional P0

**NOT READY FOR FABRICATION. RV1 is a reserved-space placeholder, not a verified trimmer footprint.**

Prepared for the college etching process planned for Friday, 30 October 2026. Source: `../schematics/diode_comp_mirror_enhanced_v2.asc`. This is the physical PCB translation of that circuit, with a power connector and voltage test points added. No extra fuse or protection network was added.

## Open the project

Open `current_mirror.kicad_pro` in KiCad 10.0.7 or later. Open the schematic and PCB from the project manager. The project-specific footprint library is registered by `fp-lib-table`.

To view the assembled board in 3D, open `current_mirror.kicad_pcb` in the PCB Editor, then choose **View → 3D Viewer**, or press **Alt+3**. You do not need to open a separate model file. The standard parts use the installed KiCad 3D models; RV1 deliberately has no body model while its footprint is unknown, and the test points appear as pads rather than modeled pins.

- `current_mirror.kicad_sch`: editable schematic; equal net labels connect electrically.
- `current_mirror.kicad_pcb`: editable, routed board.
- `Project.pretty/RV1_PENDING.kicad_mod`: deliberately provisional trimmer footprint.
- `components.json` and `BOM.csv`: connections, assumed footprints, and component list.
- `previews/`: schematic and board drawings for review.
- `reports/`: source connectivity, KiCad ERC/DRC and routing reports.
- `fabrication/`: print guidance only at P0; production copper masks are withheld until RV1 is confirmed.
- `scripts/`: reproducible generation, routing, and preview helpers.

## Completed validation for P0

Checks run with KiCad 10.0.7 on 28 October 2026:

| Check | Result |
|---|---|
| Independent extraction of original LTspice connectivity | PASS |
| KiCad schematic ERC | 0 errors, 0 warnings |
| KiCad PCB DRC | 0 errors, 0 warnings |
| Unconnected PCB items | 0 |
| Schematic-to-PCB parity issues | 0 |
| Native exported schematic netlist vs board pads | Exact match |
| Routed layers / vias / wire jumpers | B.Cu only / 0 / 0 |

These results apply to the provisional geometry; they do **not** verify that the unknown real trimmer fits. No physical assembly, fabrication, or circuit measurement has occurred. Design/source hashes are recorded in `reports/design_sha256.json`.

## Board construction

Board outline: **78 × 67 mm**. Through-hole parts on the front; **all routed copper is B.Cu** (bottom). Tracks are 0.6 mm wide; the configured minimum copper clearance is 0.4 mm. There are no vias, ground pours, or wire jumpers. Through-hole pads appear on both copper layers in KiCad's normal two-layer data model; the front is not routed and must not be used as a second fabricated copper pattern.

The layout favors generous spacing for hand assembly and chemical etching. Confirm the college machine/process can achieve these dimensions. Reference designators and assembly text are on the top silkscreen drawing; college fabrication may not produce a physical silkscreen.

All board footprints are included in `Project.pretty` as local etching variants, based on the stock footprint names recorded in `components.json`. This preserves the enlarged pads and avoids depending on changed stock-library copies. Some diode/capacitor body graphics are on F.Fab to keep them clear of the larger pads; use `previews/assembly_top.pdf` for polarity and body orientation.

## Exact electrical translation

| KiCad reference | LTspice reference | Value / role |
|---|---|---|
| J1 | V1 | External regulated 12 V DC supply connection replaces ideal source |
| R1 | F1 | **1 ohm, 1/4 W resistor**, not a fuse |
| D4 | D4 | 1N4007, series input diode |
| R2 | Rs | 620 ohm, 1/4 W |
| D3 | Dz | BZX55C5V1, 5.1 V Zener |
| D1, D2 | D1, D2 | 1N4148 |
| R3 | R1a | 1 kohm, 1/4 W |
| RV1 | RV1 | 500 ohm multiturn trimmer; simulated resistance 119.8 ohm |
| Q1, Q2 | Q1, Q2 | 2N3904 |
| R4, R5 | Re1, Re2 | 22 ohm, 1/4 W |
| R6 | Rload | 1 kohm, 1/4 W load, retained on board |
| C1 | C1 | 100 nF, at least 25 V |

Input path is J1 pin 1 (VIN) → R1 → D4 anode → D4 cathode → VCC. J1 pin 2 is GND. D4 provides series reverse-polarity blocking; R1 is not a fuse and this circuit has no added overcurrent limiter.

Q1 is diode-connected: its collector and base share BASE. Q2's base also connects to BASE. The emitter resistors remain separate. The Zener cathode is at VA; its anode connects to the anode of D1; D1 cathode connects to D2 anode; D2 cathode is grounded.

An independent extraction of LTspice wire geometry and symbol pin locations checks this mapping in `reports/source_connectivity.json`. No new SPICE simulation has been run. The existing LTspice log reports approximately 4.99945 mA at 25 °C and 5.00011 mA at 75 °C; these are source simulation results, not measured PCB performance. The actual Zener, resistor tolerances, transistor matching, and thermal arrangement can change the result.

## Trimmer reservation — must finish before Friday fabrication

**Photo update, 28 October:** the green round part and reported approximately 7.5 mm size resemble an RM065-style **single-turn** preset, rather than the inventory's multiturn description. This identification is tentative. The actual resistance and lead spacing remain unconfirmed, so the footprint has not been changed. See `reports/trimmer_photo_review.md` for the datasheet comparison and what to verify.

RV1 has an **18 × 14 mm reserved area**, shown on the user drawing layer. Its present three holes at 2.54 mm pitch are merely an editable connection placeholder. **Do not assume the actual trimmer fits these holes or this reserved area.**

The electrical plan is a rheostat: pin 1 → TRIM_TOP; pin 2 (wiper) → BASE; pin 3 → BASE. The unused end is tied to the wiper. The real manufacturer's pin numbering and footprint must be verified before transferring that plan to the final part. The approximately 119.8 ohm setting is between TRIM_TOP and BASE, not necessarily the resistance between any arbitrary pair of physical legs.

When the actual part arrives:

1. Identify its model, pin pitch, body dimensions, screw access and wiper pin.
2. Replace RV1's placeholder **in both the schematic and PCB** with the correct footprint; preserve the pin-to-net function above.
3. Adjust placement and nearby tracks within the reserved area; enlarge/move parts if necessary.
4. Rerun ERC, PCB DRC with schematic parity, and the bottom-layer/no-via checks.
5. Update the README and board revision, remove the provisional status, and only then generate the actual copper mask.

The generation scripts intentionally recreate the P0 placeholder. **Do not rerun them over a manually finalized board without updating their component/footprint definitions first.**

## Other physical assumptions to check

- Q1/Q2 footprint assumes **pin 1 emitter, pin 2 base, pin 3 collector**, with 2.54 mm spacing after lead forming. Verify the actual manufacturer's 2N3904 pinout; orient by the package drawing, not just an online picture.
- Axial resistors use 7.62 mm hole spacing; the 1N4148 and BZX55 Zener use DO-35 footprints at 7.62 mm; the 1N4007 uses DO-41 at 10.16 mm.
- C1 assumes 5.00 mm lead spacing. Confirm the actual capacitor or select a suitable replacement footprint before drilling.
- J1 is a 2.54 mm two-pin header footprint with 1 mm drills, usable as solder-wire holes. It is **not** a 5.08 mm screw-terminal footprint. Supply attachment hardware and test-point pins are additional to the group's listed electronic components.
- Test points use 1 mm holes; wires or suitable pins can be soldered into them.
- Q1 and Q2 are placed near each other; no real thermal compensation measurement or temperature qualification has been performed.

## Power and multimeter measurements

Use an external regulated **12 V DC** bench supply: positive to J1 pin 1 / VIN, negative to J1 pin 2 / GND. Confirm pad numbers and polarity in the assembly drawing before applying power. Start with a sensible current limit on the bench supply and inspect assembly first.

| Test point | Signal | Use |
|---|---|---|
| TP1 | GND | Common reference for voltage measurements |
| TP2 | VIN | Input supply before the series resistor and diode |
| TP3 | VCC / LOAD+ | Protected supply and top of R6 |
| TP4 | VA | Zener + two-diode reference node |
| TP5 | BASE | Shared transistor bases / Q1 collector |
| TP6 | OUT / LOAD− | Q2 collector and bottom of R6 |

For current inference, set the multimeter to **DC volts**, red probe TP3 and black probe TP6. `Iout = (V(TP3) − V(TP6)) / R6`. With nominal R6 = 1000 ohm, **5.00 V corresponds to 5.00 mA**. The actual resistor tolerance affects this estimate; measure its resistance with power off if accuracy matters. Do not put a meter in current mode directly across those two test points: that would bypass the load. No series current-measurement break has been added.

Adjust RV1 carefully to target approximately 5 mA. A resistance preset near 119.8 ohm should be made with power off and preferably with the trimmer isolated from parallel circuit paths. The assembled circuit may need a different setting from the simulation.

## Fabrication handoff

Do not fabricate P0. After finalization, export **B.Cu only** as a black copper pattern at **1:1 scale**, with drill-center marks if the college wants them. Keep the outline/assembly drawing separate from the copper mask; outline graphics must not accidentally become copper. Include a separate known-length calibration mark or check the 78 × 67 mm outline print dimensions. Disable fit-to-page, shrink-to-fit and printer scaling.

Confirm whether the college uses toner transfer or photoresist, which side of the film/paper contacts the board, whether a mirrored image is required, and which mask polarity they expect. Provide clearly named mirrored/unmirrored versions only once that is established. Do not decide orientation by appearance alone. A final Gerber/drill set can also be exported if the college accepts it.

## Reproduce the provisional files

Run in PowerShell from the repository root. KiCad's bundled Python is required for the PCB API:

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\build_design.py'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\route_board.py'
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' sch erc --format json -o 'PCB layout\reports\erc.json' 'PCB layout\current_mirror.kicad_sch'
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' pcb drc --format json --schematic-parity -o 'PCB layout\reports\drc.json' 'PCB layout\current_mirror.kicad_pcb'
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' sch export netlist -o 'PCB layout\reports\current_mirror.net' 'PCB layout\current_mirror.kicad_sch'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\check_design.py'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\PCB layout\scripts\export_previews.ps1'
```

The source extraction helper also requires the installed LTspice symbol files at `%LOCALAPPDATA%\LTspice\lib\sym`. Routing uses NumPy shipped with this KiCad installation. KiCad may report registry/font cache permission messages in a restricted execution environment; check the generated reports themselves for the actual design-check results.

The optional PNG renderer uses the laptop's existing regular Python/PyMuPDF installation. KiCad itself produces the PDF exports. Copper review PDFs are deliberately stamped as drafts and include the outline; they are not production masks.

The preview command uses a process-only execution-policy setting because this laptop blocks `.ps1` execution by default; it does not change the persistent Windows execution policy.

An early routing update triggered a KiCad Python/SWIG access violation while removing existing track objects. The final router avoids that API operation by removing serialized tracks before loading the board. The corrected route completed with exit code 0, followed by the clean checks above. The project opens from saved files without needing that Python process to remain running.
