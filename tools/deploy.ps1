# Deploys ./site to Cloudflare Pages (project "buenaobra", production branch "main").
# Needs Node.js and a user env var CLOUDFLARE_API_TOKEN with Account > Cloudflare Pages > Edit.
# Usage: pwsh tools/deploy.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$token = [Environment]::GetEnvironmentVariable('CLOUDFLARE_API_TOKEN', 'User')
if (-not $token) { throw 'CLOUDFLARE_API_TOKEN is not set (user environment variable).' }
$nodeDir = 'C:\Program Files\nodejs'
if (Test-Path $nodeDir) { $env:Path = "$nodeDir;$env:Path" }
$env:CLOUDFLARE_API_TOKEN = $token
$env:CLOUDFLARE_ACCOUNT_ID = '9255fadc0a69ea9915a17ab8a2d404c8'
$env:WRANGLER_SEND_METRICS = 'false'
Push-Location $root
try {
  $dirty = git status --porcelain -- site
  if ($dirty) { Write-Warning 'site/ has uncommitted changes; deploying them anyway.' }
  $sha = git rev-parse HEAD
  $msg = (git log -1 --pretty=%s)
  npx --yes wrangler@4.20.0 pages deploy site --project-name buenaobra --branch main --commit-hash $sha --commit-message $msg
} finally { Pop-Location }
