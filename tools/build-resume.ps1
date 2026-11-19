# Renders site/resume.html to site/resume.pdf with headless Microsoft Edge.
# Run after editing the resume: pwsh tools/build-resume.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$html = Join-Path $root 'site\resume.html'
$pdf = Join-Path $root 'site\resume.pdf'
$edge = @(
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $edge) { throw 'Microsoft Edge not found.' }
$profileDir = Join-Path $env:TEMP 'edge-headless-resume'
$url = 'file:///' + ($html -replace '\\', '/')
if (Test-Path $pdf) { Remove-Item $pdf }
$p = Start-Process -FilePath $edge -Wait -PassThru -ArgumentList @(
  '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
  "--user-data-dir=$profileDir", "--print-to-pdf=$pdf", $url
)
if (-not (Test-Path $pdf)) { throw "Edge did not write $pdf (exit $($p.ExitCode))." }
$kb = [math]::Round((Get-Item $pdf).Length / 1KB)
Write-Host "Wrote $pdf ($kb KB)"
