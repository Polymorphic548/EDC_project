$ErrorActionPreference = 'Stop'
$panelRoot = Split-Path $PSScriptRoot -Parent
$panelCli = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$panelBoard = Join-Path $panelRoot 'dual_current_mirror.kicad_pcb'
& $panelCli sch export pdf -o (Join-Path $panelRoot 'previews\dual_panel_schematic.pdf') (Join-Path $panelRoot 'dual_current_mirror.kicad_sch')
if ($LASTEXITCODE -ne 0) { throw 'Panel schematic export failed.' }
& $panelCli pcb export pdf --layers 'F.Fab,F.Silkscreen,Edge.Cuts,User.Drawings' --mode-single --black-and-white --scale 1 -o (Join-Path $panelRoot 'previews\dual_panel_assembly.pdf') $panelBoard
if ($LASTEXITCODE -ne 0) { throw 'Panel assembly export failed.' }
& $panelCli pcb export pdf --layers 'B.Cu,Edge.Cuts' --mode-single --black-and-white --scale 1 -o (Join-Path $panelRoot 'previews\dual_panel_copper_review.pdf') $panelBoard
if ($LASTEXITCODE -ne 0) { throw 'Panel copper review export failed.' }
# Copper ONLY: no outline, silkscreen, user cutting guides, or assembly graphics.
& $panelCli pcb export pdf --layers 'B.Cu' --mode-single --black-and-white --drill-shape-opt 1 --scale 1 -o (Join-Path $panelRoot 'fabrication\dual_panel_BCu_unmirrored_1to1.pdf') $panelBoard
if ($LASTEXITCODE -ne 0) { throw 'Panel unmirrored mask export failed.' }
& $panelCli pcb export pdf --layers 'B.Cu' --mode-single --black-and-white --drill-shape-opt 1 --mirror --scale 1 -o (Join-Path $panelRoot 'fabrication\dual_panel_BCu_mirrored_1to1.pdf') $panelBoard
if ($LASTEXITCODE -ne 0) { throw 'Panel mirrored mask export failed.' }
& 'C:\Users\swastik\AppData\Local\Programs\Python\Python312\python.exe' -B (Join-Path $PSScriptRoot 'render_panel_previews.py')
if ($LASTEXITCODE -ne 0) { throw 'Panel rendering failed.' }
