# Branche le bureau dans Claude Code : ~/.claude/settings.json pointe vers son mod.
# Relançable : settings.json est sauvegardé avant d'être modifié.
#
#   powershell -ExecutionPolicy Bypass -File .\installer.ps1
#
# -Destination sert aux essais : installer ailleurs que dans le vrai ~/.claude.

param([string]$Destination = (Join-Path $HOME '.claude'))

$ErrorActionPreference = 'Stop'
$bureau = $PSScriptRoot
$claude = $Destination
$utf8   = New-Object System.Text.UTF8Encoding($false)   # sans BOM

New-Item -ItemType Directory -Force $claude | Out-Null

# 1. Le mod doit savoir où vit son dossier
$projetJson = '{ "dossier": "' + ($bureau -replace '\\', '/') + '" }' + "`n"
[IO.File]::WriteAllText((Join-Path $bureau 'mod\projet.json'), $projetJson, $utf8)

# 2. settings.json : on sauvegarde, on ajoute le branchement, on garde le reste
$fichierReglages = Join-Path $claude 'settings.json'
if (Test-Path $fichierReglages) {
    $sauvegarde = "$fichierReglages.avant-bureau-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
    Copy-Item $fichierReglages $sauvegarde
    Write-Host "Sauvegarde : $sauvegarde"
    $reglages = Get-Content $fichierReglages -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    $reglages = New-Object PSObject
}
function Fixer($objet, $nom, $valeur) {
    if ($objet.PSObject.Properties[$nom]) { $objet.$nom = $valeur }
    else { $objet | Add-Member -NotePropertyName $nom -NotePropertyValue $valeur }
}
if (-not $reglages.PSObject.Properties['env']) { Fixer $reglages 'env' (New-Object PSObject) }
Fixer $reglages.env 'CLAUDE_CODE_PLUGIN_DIRS' (Join-Path $bureau 'mod')
[IO.File]::WriteAllText($fichierReglages, ($reglages | ConvertTo-Json -Depth 20), $utf8)
Write-Host "Bureau branché : $bureau"

# 3. Ce dont le bureau a besoin
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Warning "Python est introuvable. Le bureau en a besoin pour /bureau (construire.py). Installe Python 3, puis : pip install pillow"
} else {
    & python -c "import PIL" 2>$null
    if ($LASTEXITCODE -ne 0) { Write-Warning "Pillow manque. Lance : pip install pillow" }
}

Write-Host ""
Write-Host "Terminé. Redémarre VS Code (ou Claude Code), puis tape /bureau."
