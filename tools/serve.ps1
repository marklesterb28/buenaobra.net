# Minimal static file server for local preview (no Python/Node needed).
param([int]$Port = 8787, [string]$Root = (Join-Path $PSScriptRoot "..\site"))
$Root = (Resolve-Path $Root).Path
$types = @{ ".html"="text/html; charset=utf-8"; ".css"="text/css"; ".js"="text/javascript"; ".svg"="image/svg+xml"; ".png"="image/png"; ".jpg"="image/jpeg"; ".webp"="image/webp"; ".pdf"="application/pdf"; ".txt"="text/plain" }
$l = [System.Net.HttpListener]::new()
$l.Prefixes.Add("http://localhost:$Port/")
$l.Start()
Write-Host "Serving $Root on http://localhost:$Port/"
while ($l.IsListening) {
  $ctx = $l.GetContext()
  $path = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath.TrimStart('/'))
  if ($path -eq "" -or $path.EndsWith("/")) { $path += "index.html" }
  $file = [IO.Path]::GetFullPath((Join-Path $Root $path))
  if ($file.StartsWith($Root) -and (Test-Path $file -PathType Leaf)) {
    $bytes = [IO.File]::ReadAllBytes($file)
    $ext = [IO.Path]::GetExtension($file).ToLower()
    $ctx.Response.ContentType = $(if ($types[$ext]) { $types[$ext] } else { "application/octet-stream" })
    $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
  } else { $ctx.Response.StatusCode = 404 }
  $ctx.Response.Close()
}
