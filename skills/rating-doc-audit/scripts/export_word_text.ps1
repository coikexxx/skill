param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$resolvedInput = (Resolve-Path -LiteralPath $InputPath).Path
$outputDirectory = Split-Path -Parent $OutputPath
if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}

$word = $null
$document = $null

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    $document = $word.Documents.Open(
        $resolvedInput,
        $false,
        $true
    )

    $wdFormatUnicodeText = 7
    $document.SaveAs([ref]$OutputPath, [ref]$wdFormatUnicodeText)

    [pscustomobject]@{
        input_path = $resolvedInput
        output_path = (Resolve-Path -LiteralPath $OutputPath).Path
    } | ConvertTo-Json -Depth 3
}
finally {
    if ($document -ne $null) {
        $document.Close($false)
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($document)
    }
    if ($word -ne $null) {
        $word.Quit()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word)
    }
    [gc]::Collect()
    [gc]::WaitForPendingFinalizers()
}
