<#
Empêche l'ordinateur de tomber en veille tant que la fenêtre reste ouverte.

L'écran peut s'éteindre et la session se verrouiller normalement :
seule la mise en veille est bloquée, pour que Claude Code continue de rouler.
Teams passe « Absent » comme d'habitude.

Usage :
    .\rester_eveille.ps1              # jusqu'à Ctrl+C ou fermeture de la fenêtre
    .\rester_eveille.ps1 -Minutes 90  # s'arrête tout seul après 90 minutes
#>
param([int]$Minutes = 0)

Add-Type -Namespace Win32 -Name Power -MemberDefinition @'
[DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@

$ES_CONTINUOUS      = [uint32]'0x80000000'
$ES_SYSTEM_REQUIRED = [uint32]'0x00000001'

$fin = if ($Minutes -gt 0) { (Get-Date).AddMinutes($Minutes) } else { $null }

if ([Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED) -eq 0) {
    Write-Error "Windows a refusé la demande."
    exit 1
}

$jusqua = if ($fin) { "jusqu'à $($fin.ToString('HH:mm'))" } else { "jusqu'à Ctrl+C" }
Write-Host "Veille bloquée $jusqua. L'écran peut s'éteindre et se verrouiller."

$debut = Get-Date

# Le témoin pour le bureau des agents : la page affiche « Anti-veille : actif »
# tant que ce fichier est rafraîchi. Fenêtre fermée d'un clic, ou script
# arrêté par le mod du bureau (qui le lance quand Claude travaille), il cesse
# de l'être et la page conclut d'elle-même que le script s'est arrêté.
$temoin = Join-Path $PSScriptRoot '..\vue\eveil.js'
function Ecrire-Temoin([bool]$isActif) {
    if (-not (Test-Path (Split-Path $temoin))) { return }
    $ms = { param($d) ([DateTimeOffset]$d).ToUnixTimeMilliseconds() }
    $finMs = if ($fin) { & $ms $fin } else { 'null' }
    $js = "window.BUREAU_EVEIL = { actif: $($isActif.ToString().ToLower()), debut: $(& $ms $debut), fin: $finMs, battement: $(& $ms (Get-Date)) };"
    [IO.File]::WriteAllText($temoin, $js)
}

# Le ménage du bureau des agents : chaque session y laisse son fichier dans
# vue/sessions/, réécrit toutes les 10 s tant qu'elle vit. Intact depuis une
# heure, c'est celui d'une session fermée ou plantée. demo.js reste.
$sessions = Join-Path $PSScriptRoot '..\vue\sessions'
if (Test-Path $sessions) {
    Get-ChildItem $sessions -Filter *.js |
        Where-Object { $_.Name -ne 'demo.js' -and $_.LastWriteTime -lt (Get-Date).AddHours(-1) } |
        Remove-Item -ErrorAction SilentlyContinue
}

try {
    while (-not $fin -or (Get-Date) -lt $fin) {
        # Le titre se voit dans la barre des tâches : c'est le témoin que le script tourne encore.
        $actif = "ACTIF depuis $([int]((Get-Date) - $debut).TotalMinutes) min"
        $Host.UI.RawUI.WindowTitle = "Veille bloquée - $actif"
        Write-Host -NoNewline "`r$actif (dernier signe de vie : $((Get-Date).ToString('HH:mm:ss')))   "
        Ecrire-Temoin $true
        Start-Sleep -Seconds 10
    }
}
finally {
    Ecrire-Temoin $false
    [void][Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS)
    $Host.UI.RawUI.WindowTitle = "Veille rétablie"
    Write-Host "`nVeille rétablie."
}
