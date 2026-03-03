param(
    [string]$Repo = "JorgeJosePereiraOliveira/PROTOTIPO_PRONTUARIOELETRONICO"
)

$ErrorActionPreference = "Stop"

function Invoke-GhApi {
    param(
        [string[]]$ArgsList
    )

    $output = & gh api @ArgsList 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "gh api failed: $($ArgsList -join ' ')`n$output"
    }
    return $output
}

$milestones = @(
    @{ Title = "Sprint 1"; Start = "2026-03-03"; End = "2026-03-04" },
    @{ Title = "Sprint 2"; Start = "2026-03-05"; End = "2026-03-06" },
    @{ Title = "Sprint 3"; Start = "2026-03-07"; End = "2026-03-08" },
    @{ Title = "Sprint 4"; Start = "2026-03-09"; End = "2026-03-10" },
    @{ Title = "Sprint 5"; Start = "2026-03-11"; End = "2026-03-11" },
    @{ Title = "Sprint 6"; Start = "2026-03-12"; End = "2026-03-12" },
    @{ Title = "Sprint 7"; Start = "2026-03-13"; End = "2026-03-13" },
    @{ Title = "Sprint 8"; Start = "2026-03-14"; End = "2026-03-15" }
)

$existing = (Invoke-GhApi @("repos/$Repo/milestones?state=all&per_page=100")) | ConvertFrom-Json

foreach ($m in $milestones) {
    $description = "Inicio: $($m.Start)`nFim: $($m.End)"
    $dueOn = "{0}T23:59:59Z" -f $m.End

    $found = $existing | Where-Object { $_.title -eq $m.Title } | Select-Object -First 1

    if ($null -ne $found) {
        Invoke-GhApi @(
            "repos/$Repo/milestones/$($found.number)",
            "--method", "PATCH",
            "-f", "title=$($m.Title)",
            "-f", "description=$description",
            "-f", "due_on=$dueOn"
        ) | Out-Null
        Write-Host "Updated: $($m.Title)"
    }
    else {
        Invoke-GhApi @(
            "repos/$Repo/milestones",
            "--method", "POST",
            "-f", "title=$($m.Title)",
            "-f", "description=$description",
            "-f", "due_on=$dueOn"
        ) | Out-Null
        Write-Host "Created: $($m.Title)"
    }
}

Write-Host "Milestones process finished for $Repo"
