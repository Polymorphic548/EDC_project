# Single-layer current mirror - P3 source values synced

The current design uses **R7, a single nominal 120 ohm fixed resistor**, in place of RV1. The user's supplied resistor measured **117.6 ohm**. There is no trimmer in the active schematic, PCB or BOM, so no wiper identification is required.

## Open and review

Open `current_mirror.kicad_pro`, then `current_mirror.kicad_pcb` in KiCad 10.0.7 or later. **Alt+3** opens the 3D Viewer. The new R7 has a standard axial resistor model. Review drawings are in `previews/`; they are not production copper masks.

## Circuit change

R7 connects **TRIM_TOP -> 120 ohm -> BASE**, replacing the two-terminal resistance formerly supplied by LTspice RV1. TRIM_TOP is retained as a legacy net name for the R3/R7 junction. R7 has two pads, no polarity and no wiper/end jumper.

The user updated the LTspice files on 30 October: supply 9.8 V, Rs 662 ohm, C1 1.33 nF and RV parameter 117.6 ohm. The PCB now follows these values, while retaining the approved fixed nominal 120 ohm part R7 with its measured 117.6 ohm value shown. Reference designators and all connections are unchanged. The supplied log reports 4.624594 mA at 25 C and 4.667352 mA at 75 C; no new simulation or physical measurement was run. All tracks, pads, placements, footprints and outline were preserved; no rerouting was performed.

| KiCad | Source reference | Value |
|---|---|---|
| J1 | Replaces V1 | 9.8 V external input |
| R1 | F1 | 1 ohm, 1/4 W resistor, not fuse |
| R2 | Rs | 662 ohm, 1/4 W |
| R3 | R1a | 1 kohm, 1/4 W |
| R4, R5 | Re1, Re2 | 22 ohm, 1/4 W |
| R6 | Rload | 1 kohm, 1/4 W |
| R7 | Replaces RV1 | 120 ohm, 1/4 W; user measured 117.6 ohm |
| D1, D2 | D1, D2 | 1N4148 |
| D3 | Dz | BZX55C5V1, 5.1 V Zener |
| D4 | D4 | 1N4007 |
| Q1, Q2 | Q1, Q2 | 2N3904 |
| C1 | C1 | 1.33 nF, at least 25 V |

All other circuit connections and component values are preserved. Q1 collector is tied to its base; Q2 collector is OUT. Q1/Q2 emitters connect through their separate 22 ohm resistors to GND. Input is J1 pin 1 -> R1 -> D4 anode -> D4 cathode -> VCC; J1 pin 2 is GND. There is no added fuse or general overcurrent protection.

## Test points

| Point | Node |
|---|---|
| TP1 | GND |
| TP2 | VIN, before R1/D4 |
| TP3 | VCC / LOAD+, after R1/D4 |
| TP4 | VA, reference node |
| TP5 | BASE, shared transistor bases and Q1 collector |
| TP6 | OUT / LOAD-, Q2 collector |

Normal operation needs no multimeter. To infer output current, use DC volts: red TP3, black TP6. `Iout = (V(TP3)-V(TP6))/R6`. With nominal 1 kohm R6, 5 V corresponds to 5 mA. Do not use current mode across TP3/TP6. R7 is fixed, so there is no adjustment screw.

## Board and files

- Board remains **78 x 67 mm**, through-hole, bottom copper only.
- Tracks 0.6 mm; configured minimum clearance 0.4 mm; no vias, jumpers or pours.
- R7 uses `Project:R7_ETCH`, based on the same 7.62 mm axial quarter-watt footprint as the other resistors; pads 2.2 mm, drills 0.8 mm.
- `components.json` records the nominal value, reported measured value, nets, footprints and positions; `BOM.csv` lists assembly parts.
- `Project.pretty` includes current local footprints. Unused P0/P1 trimmer footprints and `previews/trimmer_fit_check.pdf` are historical and must not be used for P3 fabrication.
- `reports/P3_source_sync_2026-10-30/README.md` records the latest change; earlier P2/P1/P0 records are historical. Current machine reports are `reports/erc.json`, `reports/drc.json`, `reports/board_audit.json`, `reports/source_connectivity.json` and `reports/routing.json`.
- `reports/design_sha256.json` identifies the current source and CAD files. Historical P0/P1 reports remain dated baseline evidence.

The CAD checks verify connectivity and layout under their configured rules, not actual part fit, temperature behavior or a guaranteed 5 mA physical result. Reported old LTspice output/temperature values apply to the original simulation only.

## Physical and fabrication checks

Verify the actual 2N3904 manufacturer's pinout against **1=E, 2=B, 3=C** and form the leads for the selected wide footprint. Verify C1's assumed 5 mm lead spacing and each resistor's physical fit. J1 uses 2.54 mm spacing for a header or soldered wires, not a 5.08 mm screw-terminal block. Test points have 1 mm drills. Supply and optional test-point hardware are additional to the component inventory.

Confirm the college's etching process, mask polarity and mirror convention. After checks, export B.Cu only at 1:1 with drill-centre marks as requested; keep outline and assembly graphics separate from the copper mask. Disable printer scaling and verify dimensions. Current review PDFs contain outline/notices and are not production masks. No production mask has been released.

## Reproduce P3

Run from the repository root in PowerShell. **Back up manual edits first: regeneration overwrites schematic/board.** An existing `.kicad_pro` is preserved by the generator; KiCad CLI may normalize its UI metadata. A local pre-P3 snapshot is retained in the ignored `current_mirror-backups/before_P3_source_sync_2026-10-30/` folder. `scripts/sync_source_values.py` applies the reviewed P3 value/label changes without rerouting; full generation below rebuilds the design.

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\build_design.py'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\route_board.py'
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' sch export netlist -o 'PCB layout\reports\current_mirror.net' 'PCB layout\current_mirror.kicad_sch'
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' sch erc --format json -o 'PCB layout\reports\erc.json' 'PCB layout\current_mirror.kicad_sch'
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' pcb drc --format json --schematic-parity -o 'PCB layout\reports\drc.json' 'PCB layout\current_mirror.kicad_pcb'
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -B 'PCB layout\scripts\check_design.py'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\PCB layout\scripts\export_previews.ps1'
```

Source extraction needs the installed LTspice symbols in `%LOCALAPPDATA%\LTspice\lib\sym`. Routing uses NumPy in KiCad's Python. Optional PNG rendering uses the existing regular Python/PyMuPDF installation. The process-only execution policy setting does not change the persistent Windows policy. Registry/font-cache permission messages can occur under restricted execution; inspect the actual generated ERC/DRC results.

The P1 trimmer-update helper is retired and refuses to restore the retired trimmer. KiCad/SWIG track-removal faults are avoided by stripping serialized tracks before loading/routing. Saved files do not require Python to remain running.
