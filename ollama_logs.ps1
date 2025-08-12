Write-Host "Chat log will be saved in Markdown format. Press Ctrl + C to exit."
Write-Host ""

# --- (1) Set up log root directory ---
$logFolder = "C:\ollama_logs"
if (-not (Test-Path $logFolder)) {
    New-Item -ItemType Directory -Path $logFolder | Out-Null
}

# --- (2) Retrieve model list ---
Write-Host "Fetching available model list..."

# Remove header/empty lines, extract model names only
$modelsRaw = ollama list | Select-Object -Skip 1
$models = $modelsRaw | Where-Object { $_ -ne "" } | ForEach-Object {
    ($_ -split "\s+")[0].Trim()
}

if ($models.Count -eq 0) {
    Write-Host "No models available. Please use 'ollama pull' to download models first." -ForegroundColor Red
    exit
}

# --- (3) Display models with numbers ---
Write-Host "Available models:"
for ($i = 0; $i -lt $models.Count; $i++) {
    Write-Host "[$($i+1)] $($models[$i])"
}

# --- (4) Model selection ---
do {
    $selection = Read-Host "Enter the model number to use (1-$($models.Count))"
} while (-not ($selection -match '^\d+$' -and $selection -ge 1 -and $selection -le $models.Count))

$chosenModel = $models[$selection - 1]
Write-Host "Selected model: '$chosenModel'" -ForegroundColor Green

# --- (5) Model folder & date-based log file name ---
$date = Get-Date -Format "yyyy-MM-dd"

# Clean up model name for safe filename
$AI_name = $chosenModel -replace '[\\\/:*?"<>|]', '_'

# Make model-specific folder (e.g. C:\ollama_logs\gpt-oss)
$modelFolder = Join-Path $logFolder $AI_name
if (-not (Test-Path $modelFolder)) {
    New-Item -ItemType Directory -Path $modelFolder | Out-Null
}

# File path (e.g. C:\ollama_logs\gpt-oss\2025-08-11.md)
$logFile = Join-Path $modelFolder "$date.md"

# --- (6) Initialize file with Markdown header/tags if first creation ---
if (-not (Test-Path $logFile)) {
    Add-Content $logFile "---"
    Add-Content $logFile "tags:"
    Add-Content $logFile "  - log"
    Add-Content $logFile "  - AI"
    Add-Content $logFile "  - $chosenModel"
    Add-Content $logFile "---"
    Add-Content $logFile "# ollama_log_$date"
}

# --- (7) Conversation loop ---
while ($true) {
    # User input
    $userInput = Read-Host "User"
    if ([string]::IsNullOrWhiteSpace($userInput)) { continue }

    # Send to Ollama
    $response = ollama run $chosenModel $userInput

    # Log in Markdown style
    $timestamp = Get-Date -Format "HH:mm:ss"
    Add-Content $logFile "## [$timestamp]"
    Add-Content $logFile "**User:** $userInput"
    Add-Content $logFile ""
    Add-Content $logFile "**AI:** $response"
    Add-Content $logFile "`n---`n"

    # Output to console
    Write-Host "AI: $response"
}