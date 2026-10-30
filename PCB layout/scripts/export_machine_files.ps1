$ErrorActionPreference = 'Stop'
$machineRoot = Split-Path $PSScriptRoot -Parent
$machineCli = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$machineBoard = Join-Path $machineRoot 'dual_current_mirror.kicad_pcb'
$machineOutput = Join-Path $machineRoot 'fabrication\machine_files'
New-Item -ItemType Directory -Path $machineOutput -Force | Out-Null
# Standard RS-274X, .gbr filenames, no front copper, no mask/silk/common layers.
# Both exports use KiCad's absolute origin, millimetres, and NO extra mirroring.
& $machineCli pcb export gerbers --layers 'B.Cu,Edge.Cuts' --no-protel-ext --no-x2 --no-netlist --disable-aperture-macros --precision 6 -o $machineOutput $machineBoard
if ($LASTEXITCODE -ne 0) { throw 'Gerber export failed.' }
& $machineCli pcb export drill --format excellon --drill-origin absolute --excellon-units mm --excellon-zeros-format decimal --generate-map --map-format pdf --generate-report --report-path (Join-Path $machineOutput 'drill_report.rpt') -o $machineOutput $machineBoard
if ($LASTEXITCODE -ne 0) { throw 'Excellon drill export failed.' }
# The KiCad data model has two pad copper layers, but this physical job has
# ONE copper face. Do not distribute its automatic two-layer job metadata.
$machineJob = Join-Path $machineOutput 'dual_current_mirror-job.gbrjob'
if (Test-Path -LiteralPath $machineJob) { Remove-Item -LiteralPath $machineJob }
