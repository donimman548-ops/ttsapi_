param(
    [string]$Python = "python",
    [string]$Venv = ".venv-xtts"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Push-Location $root
try {
    & $Python --version
    & $Python -m venv $Venv
    & ".\$Venv\Scripts\python.exe" -m pip install --upgrade pip wheel setuptools
    & ".\$Venv\Scripts\python.exe" -m pip install -r requirements.txt
    & ".\$Venv\Scripts\python.exe" -m pip install -r requirements-xtts.txt
    Write-Host "XTTS environment ready. Set TTS_ENGINE=xtts in .env and run scripts\test_xtts.py."
}
finally {
    Pop-Location
}
