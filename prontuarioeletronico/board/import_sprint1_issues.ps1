param(
    [string]$Repo = "JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO",
    [string]$CsvPath = "prontuarioeletronico/board/board_backlog_github_issues_ready.csv",
    [string]$TargetMilestone = "Sprint 1",
    [switch]$DryRun
)

Write-Host "[DEPRECATION] Use preferencialmente: prontuarioeletronico/board/import_sprint_issues.ps1"
& "prontuarioeletronico/board/import_sprint_issues.ps1" -Repo $Repo -CsvPath $CsvPath -TargetMilestone $TargetMilestone -DryRun:$DryRun
exit $LASTEXITCODE

$ErrorActionPreference = "Stop"

function Invoke-Gh {
    param(
        [string[]]$GhArgs
    )

    $output = & gh @GhArgs 2>&1
    $exitCode = $LASTEXITCODE

    return [PSCustomObject]@{
        ExitCode = $exitCode
        Output = $output
    }
}

function Test-GhAuth {
    $result = Invoke-Gh @("auth", "status")
    if ($result.ExitCode -ne 0) {
        throw "GitHub CLI não autenticado. Execute: gh auth login"
    }
}

function Get-LabelColor {
    param([string]$Label)

    if ($Label -like "priority:p0") { return "B60205" } # vermelho
    if ($Label -like "priority:p1") { return "D93F0B" } # laranja
    if ($Label -like "epic:*")      { return "5319E7" } # roxo
    if ($Label -like "sprint:*")    { return "1D76DB" } # azul
    if ($Label -like "sp:*")        { return "0E8A16" } # verde
    return "1D76DB"
}

Write-Host "[1/6] Validando autenticação no GitHub CLI..."
Test-GhAuth

Write-Host "[2/6] Validando arquivo CSV..."
if (-not (Test-Path $CsvPath)) {
    throw "CSV não encontrado: $CsvPath"
}

$rows = Import-Csv $CsvPath | Where-Object { $_.Milestone -eq $TargetMilestone }
if (-not $rows -or $rows.Count -eq 0) {
    throw "Nenhuma issue encontrada no CSV para milestone '$TargetMilestone'."
}

Write-Host "[3/6] Coletando labels do CSV e criando as ausentes..."
$labelsFromCsv = $rows |
    ForEach-Object { $_.Labels -split "," } |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -ne "" } |
    Sort-Object -Unique

$existingLabelsResult = Invoke-Gh @("label", "list", "--repo", $Repo, "--limit", "1000", "--json", "name")
if ($existingLabelsResult.ExitCode -ne 0) {
    throw "Falha ao listar labels existentes: $($existingLabelsResult.Output)"
}

try {
    $existingLabels = ($existingLabelsResult.Output | ConvertFrom-Json | ForEach-Object { $_.name })
}
catch {
    $fallback = Invoke-Gh @("label", "list", "--repo", $Repo, "--limit", "1000")
    if ($fallback.ExitCode -ne 0) {
        throw "Falha ao listar labels (fallback): $($fallback.Output)"
    }
    $existingLabels = @()
    foreach ($line in ($fallback.Output -split "`r?`n")) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        $firstToken = ($line -split "\s+")[0]
        if (-not [string]::IsNullOrWhiteSpace($firstToken) -and $firstToken -ne "NAME") {
            $existingLabels += $firstToken
        }
    }
}

foreach ($lb in $labelsFromCsv) {
    if ($existingLabels -contains $lb) {
        continue
    }

    $color = Get-LabelColor -Label $lb

    if ($DryRun) {
        Write-Host "[DRY-RUN] Criaria label: $lb"
        continue
    }

    $createLabel = Invoke-Gh @(
        "label", "create", $lb,
        "--repo", $Repo,
        "--color", $color,
        "--description", "Label de backlog importado"
    )

    if ($createLabel.ExitCode -ne 0) {
        throw "Falha ao criar label '$lb': $($createLabel.Output)"
    }

    Write-Host "Label criada: $lb"
}

Write-Host "[4/6] Lendo issues já existentes na milestone para importação idempotente..."
$existingIssuesResult = Invoke-Gh @("issue", "list", "--repo", $Repo, "--milestone", $TargetMilestone, "--limit", "500", "--json", "title")
if ($existingIssuesResult.ExitCode -ne 0) {
    throw "Falha ao listar issues existentes: $($existingIssuesResult.Output)"
}

$existingTitles = ($existingIssuesResult.Output | ConvertFrom-Json | ForEach-Object { $_.title })

Write-Host "[5/6] Importando issues da milestone '$TargetMilestone'..."
$created = 0
$skipped = 0
$errors = 0

foreach ($r in $rows) {
    if ($existingTitles -contains $r.Title) {
        Write-Host "SKIP (já existe): $($r.Title)"
        $skipped++
        continue
    }

    $body = $r.Body -replace "\\n", "`n"
    $labels = @()
    if (-not [string]::IsNullOrWhiteSpace($r.Labels)) {
        $labels = $r.Labels.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
    }

    $issueArgs = @(
        "issue", "create",
        "--repo", $Repo,
        "--title", $r.Title,
        "--body", $body,
        "--milestone", $r.Milestone,
        "--assignee", $r.Assignees
    )

    foreach ($lb in $labels) {
        $issueArgs += @("--label", $lb)
    }

    if ($DryRun) {
        Write-Host "[DRY-RUN] Criaria issue: $($r.Title)"
        $created++
        continue
    }

    $createIssue = Invoke-Gh $issueArgs

    if ($createIssue.ExitCode -ne 0) {
        Write-Host "ERROR ao criar '$($r.Title)':"
        Write-Host $createIssue.Output
        $errors++
        continue
    }

    Write-Host "CREATED: $($r.Title)"
    $created++
}

Write-Host "[6/6] Resumo"
Write-Host "- Milestone alvo : $TargetMilestone"
Write-Host "- Criadas        : $created"
Write-Host "- Ignoradas      : $skipped"
Write-Host "- Erros          : $errors"

if ($errors -gt 0) {
    throw "Importação finalizada com erros."
}

Write-Host "Importação concluída com sucesso."
