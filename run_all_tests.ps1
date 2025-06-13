# Pfad zu den Tests
$testDir = "backend/tests"
$testFiles = @(
    "test_cable_diagnostics.py",
    "test_ipv6_tools.py",
    "test_event_trigger.py",
    "test_device_health.py",
    "test_scheduled_tasks.py",
    "test_incidents.py",
    "test_ping_tool.py"
)

Write-Host "`nStarte Tests..." -ForegroundColor Cyan

foreach ($testFile in $testFiles) {
    $fullPath = Join-Path $testDir $testFile
    Write-Host "`n>>> Teste: $testFile" -ForegroundColor Yellow
    pytest $fullPath
}

Write-Host "`nAlle Tests abgeschlossen." -ForegroundColor Green
