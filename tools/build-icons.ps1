# Builds site/assets/icons/*.svg from Iconify JSON sets (downloaded separately).
# Usage: pwsh tools/build-icons.ps1 -SetsDir <folder with selfhst.json, logos.json, ...>
param([Parameter(Mandatory)][string]$SetsDir, [string]$Out = (Join-Path $PSScriptRoot "..\site\assets\icons"))

# file name = set:icon [| color for single-color icons]
$map = [ordered]@{
  'm365'         = 'selfhst:microsoft-365'
  'outlook'      = 'selfhst:microsoft-outlook'
  'teams'        = 'selfhst:microsoft-teams'
  'sharepoint'   = 'selfhst:microsoft-sharepoint'
  'onedrive'     = 'selfhst:microsoft-onedrive'
  'exchange'     = 'simple-icons:microsoftexchange|#1a8cff'
  'entra'        = 'selfhst:microsoft-entra-id'
  'ad'           = 'mdi:account-network|#4fb3ff'
  'gpo'          = 'mdi:file-cog|#9aa7ff'
  'mimecast'     = 'mdi:email-lock|#3dff8f'
  'appriver'     = 'mdi:shield-check|#00e8ff'
  'emailauth'    = 'mdi:email-check|#f7e463'
  'slack'        = 'logos:slack-icon'
  'cloudflare'   = 'logos:cloudflare-icon'
  'tailscale'    = 'simple-icons:tailscale|#e8e8f0'
  'adguard'      = 'selfhst:adguard-home'
  'forgejo'      = 'selfhst:forgejo'
  'gatus'        = 'selfhst:gatus'
  'ntfy'         = 'selfhst:ntfy'
  'beszel'       = 'selfhst:beszel'
  'vaultwarden'  = 'selfhst:vaultwarden-light'
  'itflow'       = 'mdi:ticket-account|#3dff8f'
  'jellyfin'     = 'selfhst:jellyfin'
  'navidrome'    = 'selfhst:navidrome'
  'chorecast'    = 'lucide:list-checks|#f7e463'
  'phone'        = 'lucide:smartphone|#e8e8f0'
  'visitor'      = 'lucide:users-round|#e8e8f0'
  # toolbox
  'okta'         = 'simple-icons:okta|#4d8cff'
  'duo'          = 'mdi:cellphone-key|#6bd425'
  'cyberark'     = 'mdi:safe-square|#3d8bff'
  '1password'    = 'simple-icons:1password|#3b82f6'
  'lastpass'     = 'mdi:lastpass|#ff4d4d'
  'defender'     = 'selfhst:microsoft-defender'
  'sentinelone'  = 'mdi:shield-half-full|#a78bfa'
  'crowdstrike'  = 'selfhst:crowdstrike'
  'aurora'       = 'mdi:shield-bug|#ff4d4d'
  'webroot'      = 'mdi:shield-account|#4ade80'
  'bitlocker'    = 'mdi:lock-check|#f7e463'
  'usecure'      = 'mdi:school|#ff2bd6'
  'proofpoint'   = 'mdi:email-alert|#3dc4ff'
  'avanan'       = 'mdi:cloud-lock|#ff8a3d'
  'barracuda'    = 'mdi:fish|#4d9be6'
  'msgtrace'     = 'mdi:email-search|#1a8cff'
  'teamviewer'   = 'simple-icons:teamviewer|#2b8cff'
  'anydesk'      = 'simple-icons:anydesk|#ef443b'
  'splashtop'    = 'mdi:monitor-share|#4ade80'
  'beyondtrust'  = 'mdi:shield-key|#ff8a3d'
  'jamf'         = 'mdi:cellphone-cog|#a3e635'
  'sccm'         = 'mdi:package-down|#4fb3ff'
  'w365'         = 'lucide:monitor-cloud|#00e8ff'
  'meraki'       = 'simple-icons:cisco|#1ba0d7'
  'fortinet'     = 'selfhst:fortinet'
  'sonicwall'    = 'mdi:wall-fire|#ff8a3d'
  'paloalto'     = 'simple-icons:paloaltonetworks|#fa582d'
  'pfsense'      = 'simple-icons:pfsense|#4d9be6'
  'backup'       = 'mdi:backup-restore|#2a9df4'
  'veeam'        = 'mdi:server-security|#00b336'
  'acronis'      = 'mdi:cloud-upload|#4fb3ff'
  'prtg'         = 'mdi:chart-line|#3dff8f'
  'confluence'   = 'logos:confluence'
  'zoom'         = 'logos:zoom-icon'
  'webex'        = 'simple-icons:webex|#4de1c1'
  'ringcentral'  = 'mdi:phone-voip|#ff8a3d'
  'docusign'     = 'simple-icons:docusign|#ffcc22'
  'acrobat'      = 'selfhst:adobe-acrobat'
  'dropbox'      = 'logos:dropbox'
  'box'          = 'simple-icons:box|#2b8cff'
  'windows'      = 'logos:microsoft-windows-icon'
  'apple'        = 'simple-icons:apple|#e8e8f0'
  'servicenow'   = 'devicon:servicenow'
  'jira'         = 'logos:jira'
  'autotask'     = 'cib:autotask|#ff8a3d'
  'kaseya'       = 'mdi:remote-desktop|#3dc4ff'
  'datto'        = 'mdi:monitor-dashboard|#2a9df4'
  'logicmonitor' = 'lucide:activity|#ff2bd6'
  'itglue'       = 'selfhst:it-glue-light'
  'onboarding'   = 'lucide:user-round-plus|#00e8ff'
  'intune'       = 'mdi:laptop-account|#2fa8ff'
  'linux'        = 'logos:linux-tux'
  'docker'       = 'logos:docker-icon'
  'proxmox'      = 'selfhst:proxmox'
  'caddy'        = 'selfhst:caddy'
  'dns'          = 'lucide:globe|#00e8ff'
  'gworkspace'   = 'logos:google-icon'
  'ubiquiti'     = 'simple-icons:ubiquiti|#2b8cff'
  'vmware'       = 'selfhst:vmware-esx-light'
  'citrix'       = 'simple-icons:citrix|#4d9be6'
  'hyperv'       = 'devicon:hyperv'
  'powershell'   = 'simple-icons:powershell|#5391fe'
  'network'      = 'lucide:network|#00e8ff'
  'ansible'      = 'simple-icons:ansible|#ff4d4d'
  'azure'        = 'devicon:azure'
  'ear'          = 'lucide:ear|#ff2bd6'
  'teach'        = 'lucide:graduation-cap|#f7e463'
  'kb'           = 'lucide:notebook-pen|#3dff8f'
  'team'         = 'lucide:users|#00e8ff'
  'calm'         = 'lucide:heart-handshake|#ff2bd6'
  'keyboard'     = 'lucide:keyboard|#f7e463'
}

$sets = @{}
New-Item -ItemType Directory -Force $Out | Out-Null
foreach ($file in $map.Keys) {
  $spec, $color = $map[$file] -split '\|'
  $set, $name = $spec -split ':', 2
  if (-not $sets[$set]) { $sets[$set] = Get-Content (Join-Path $SetsDir "$set.json") -Raw | ConvertFrom-Json -AsHashtable }
  $s = $sets[$set]
  $n = $name; $guard = 0
  while (-not $s.icons[$n] -and $s.aliases -and $s.aliases[$n] -and $guard++ -lt 5) { $n = $s.aliases[$n].parent }
  $icon = $s.icons[$n]
  if (-not $icon) { Write-Warning "missing $spec"; continue }
  $w = $icon.width ?? $s.width ?? 16; $h = $icon.height ?? $s.height ?? 16
  $body = $icon.body
  if ($color) { $body = $body -replace 'currentColor', $color }
  $svg = "<svg xmlns=`"http://www.w3.org/2000/svg`" viewBox=`"$($icon.left ?? 0) $($icon.top ?? 0) $w $h`">$body</svg>"
  if (-not $color -and $svg -match 'currentColor') { Write-Warning "$file still uses currentColor" }
  [IO.File]::WriteAllText((Join-Path $Out "$file.svg"), $svg)
}
"wrote $((Get-ChildItem $Out -Filter *.svg).Count) icons to $Out"
