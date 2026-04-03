param(
    [string]$Workspace = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function To-JsonValue {
    param(
        [Parameter(Mandatory = $true)]
        $Value
    )

    return ($Value | ConvertTo-Json -Depth 8 -Compress)
}

function Get-CandidateFiles {
    param(
        [string]$BasePath,
        [string[]]$Extensions
    )

    if (-not (Test-Path -LiteralPath $BasePath)) {
        return [System.Collections.ArrayList]::new()
    }

    $allowed = @{}
    foreach ($ext in $Extensions) {
        $allowed[$ext.ToLowerInvariant()] = $true
    }

    $items = Get-ChildItem -LiteralPath $BasePath -Recurse -File | Where-Object {
        $ext = $_.Extension.ToLowerInvariant()
        $allowed.ContainsKey($ext)
    } | Sort-Object FullName

    $index = 1
    $results = [System.Collections.ArrayList]::new()
    foreach ($item in $items) {
        [void]$results.Add([ordered]@{
            index = $index
            name = $item.Name
            full_path = $item.FullName
            extension = $item.Extension
            size_bytes = [int64]$item.Length
            size_mb = [math]::Round($item.Length / 1MB, 2)
            last_write_time = $item.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        })
        $index++
    }

    return $results
}

$reviewFolder = Join-Path $Workspace "评级审核文件"
$standardFolder = Join-Path $Workspace "评级标准文件"

$workspacePath = (Resolve-Path -LiteralPath $Workspace).Path
$reviewExists = Test-Path -LiteralPath $reviewFolder
$standardExists = Test-Path -LiteralPath $standardFolder
$reviewFiles = Get-CandidateFiles -BasePath $reviewFolder -Extensions @(".doc", ".docx")
$standardFiles = Get-CandidateFiles -BasePath $standardFolder -Extensions @(".xls", ".xlsx", ".xlsm")

$reviewFilesJson = if ($reviewFiles.Count -eq 0) { "[]" } else { To-JsonValue -Value $reviewFiles }
$standardFilesJson = if ($standardFiles.Count -eq 0) { "[]" } else { To-JsonValue -Value $standardFiles }

$json = @"
{
  "workspace": $(To-JsonValue -Value $workspacePath),
  "review_folder": {
    "path": $(To-JsonValue -Value $reviewFolder),
    "exists": $(To-JsonValue -Value $reviewExists),
    "files": $reviewFilesJson
  },
  "standard_folder": {
    "path": $(To-JsonValue -Value $standardFolder),
    "exists": $(To-JsonValue -Value $standardExists),
    "files": $standardFilesJson
  }
}
"@

$json
