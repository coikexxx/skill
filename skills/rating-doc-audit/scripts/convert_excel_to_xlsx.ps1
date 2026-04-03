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

$excel = $null
$workbook = $null

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    $workbook = $excel.Workbooks.Open($resolvedInput, 0, $true)
    $xlOpenXMLWorkbook = 51
    $workbook.SaveAs($OutputPath, $xlOpenXMLWorkbook)

    [pscustomobject]@{
        input_path = $resolvedInput
        output_path = (Resolve-Path -LiteralPath $OutputPath).Path
    } | ConvertTo-Json -Depth 3
}
finally {
    if ($workbook -ne $null) {
        $workbook.Close($false)
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($workbook)
    }
    if ($excel -ne $null) {
        $excel.Quit()
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel)
    }
    [gc]::Collect()
    [gc]::WaitForPendingFinalizers()
}
