$ErrorActionPreference = 'Stop'
$pcbRoot = Split-Path $PSScriptRoot -Parent
$pcbCli = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
& $pcbCli sch export pdf -o (Join-Path $pcbRoot 'previews\schematic.pdf') (Join-Path $pcbRoot 'current_mirror.kicad_sch')
if ($LASTEXITCODE -ne 0) { throw 'Schematic PDF export failed.' }
& $pcbCli pcb export pdf --layers 'F.Fab,F.Silkscreen,Edge.Cuts,User.Drawings' --mode-single --black-and-white --scale 1 -o (Join-Path $pcbRoot 'previews\assembly_top.pdf') (Join-Path $pcbRoot 'current_mirror.kicad_pcb')
if ($LASTEXITCODE -ne 0) { throw 'Assembly PDF export failed.' }
& $pcbCli pcb export pdf --layers 'B.Cu,Edge.Cuts' --mode-single --black-and-white --scale 1 -o (Join-Path $pcbRoot 'previews\copper_review.pdf') (Join-Path $pcbRoot 'current_mirror.kicad_pcb')
if ($LASTEXITCODE -ne 0) { throw 'Copper review PDF export failed.' }
# Use the regular Python environment, which has PyMuPDF installed on this laptop.
& 'C:\Users\swastik\AppData\Local\Programs\Python\Python312\python.exe' -B (Join-Path $PSScriptRoot 'render_previews.py')
if ($LASTEXITCODE -ne 0) { throw 'PNG rendering failed.' }
